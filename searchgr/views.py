from django.shortcuts import render, get_object_or_404
from news.models import News
from events.models import Event
from .models import SettingsSearch
from directions.models import Trend, Direction
from django.db.models import Q, Sum
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity
from rest_framework import views
from rest_framework.response import Response
from datetime import date, datetime
import re

def SortByRank(listEntry):
    return listEntry['rank']

def ResultDictBuilder(result_dict):
    r_array = list()
    keys = result_dict.keys()
    for key in keys:
        r_array.append(result_dict.get(key))
    r_array.sort(reverse=True, key=SortByRank)
    for r in r_array:
        del r["rank"]
    return r_array

class SearchView(views.APIView):
    def get(self, request, page):
        offset = int(page)
        result_dict = dict()
        dominantEssence = request.GET.get("p", "-")
        settings = SettingsSearch.objects.first()
        # =====================================================================================================
        # ======================================== Parse input string =========================================
        # =====================================================================================================
        query = request.GET.get("q","-")
        query = query.translate(str.maketrans("", "", "!@#$%^&*_+|+\/:;[]{}<>,."))
        query = re.sub( '\s+', ' ', query).strip()
        Directions = Direction.objects.all()
        if query == "направления":
            i = 0
            for entry in Trend.objects.all():
                result_dict['/trend/' + str(entry.id)] = {
                    'id': entry.id,
                    'rank': i,
                    'title': entry.title,
                    'titlePreview': None,
                    'type': 'direction'
                }
                i -= 1
        elif query == "новости":
            i = 0
            for entry in News.objects.all():
                result_dict['/news/' + str(entry.id)] = {
                    'id': entry.id,
                    'rank': i,
                    'title': entry.title,
                    'titlePreview': None,
                    'type': 'news'
                }
                i -= 1
        elif query == "события":
            i = 0
            for entry in Event.objects.all():
                result_dict['/event/' + str(entry.id)] = {
                    'id': entry.id,
                    'rank': i,
                    'title': entry.title,
                    'titlePreview': None,
                    'type': 'events'
                }
                i -= 1
        elif Directions.filter(title = query).count() > 0:
            counterNews, counterEvent = 0, 0
            for entry in News.objects.filter(directions = Directions.get(title=query)):
                result_dict['/news/' + str(entry.id)] = {
                    'id': entry.id,
                    'rank': counterNews,
                    'title': entry.title,
                    'titlePreview': None,
                    'type': 'news'
                }
                counterNews -= 1
            for entry in Event.objects.filter(directions=Directions.get(title=query)):
                result_dict['/event/' + str(entry.id)] = {
                    'id': entry.id,
                    'rank': counterEvent,
                    'title': entry.title,
                    'titlePreview': None,
                    'type': 'events'
                }
                counterEvent -= 1
            counterNews, counterEvent = abs(counterNews), abs(counterEvent)
            for key in result_dict.keys():
                elem = result_dict.get(key)
                if dominantEssence == elem["type"]:
                    elem["rank"] += counterNews if dominantEssence == "news" else counterEvent if dominantEssence == "events" else 0
        else:
            query_dict = query.split(" ")
            len_dict = len(query_dict)
            i = 1
            while i < len_dict:
                j = 0
                while j < len_dict-i:
                    word = ""
                    l = 0
                    while l <= i:
                        word += query_dict[l+j] + " "
                        l+=1
                    query_dict.append(word[:-1])
                    j+=1
                i+=1
            # =====================================================================================================
            # =================================== Search query inside News ========================================
            # =====================================================================================================
            vectorTitle = SearchVector('title')
            vectorPreview = SearchVector('preview')
            vector = SearchVector('text')
            for word in query_dict:
                que = SearchQuery(word)
                news_temp = News.objects.annotate(qTitle=SearchRank(vectorTitle, que), qPreview=SearchRank(vectorPreview, que), qText = SearchRank(vector, que))
                for entry in news_temp:
                    entry.rank = round(entry.qTitle * settings.factorTitle + entry.qPreview * settings.factorPreview + entry.qText * settings.factorText, 4)

                    if entry.rank >= settings.filterGTE:
                        if dominantEssence == "news":
                            entry.rank += settings.factorPage
                        result_dict['/news/' + str(entry.id)] = {
                            'id': entry.id,
                            'rank': entry.rank,
                            'title': entry.title,
                            'titlePreview': entry.preview,
                            'type': 'news'
                        }
            # =====================================================================================================
            # =============================== Search query inside Events ==========================================
            # =====================================================================================================
            vectorTitle = SearchVector('title')
            vector = SearchVector('text')
            for word in query_dict:
                que = SearchQuery(word)
                event_temp = Event.objects.annotate(qTitle=SearchRank(vectorTitle, que), qText=SearchRank(vector, que))
                for entry in event_temp:
                    entry.rank = round(entry.qTitle * (settings.factorTitle + settings.factorPreview) + entry.qText * settings.factorText, 4)

                    if entry.rank >= settings.filterGTE:
                        if dominantEssence == "events":
                            entry.rank += settings.factorPage
                        result_dict['/event/' + str(entry.id)] = {
                            'id': entry.id,
                            'rank': entry.rank,
                            'title': entry.title,
                            'titlePreview': None,
                            'type': 'events'
                        }
            # =====================================================================================================
            # =================================== Search query inside Trends ======================================
            # =====================================================================================================
            vectorTitle = SearchVector('title')
            vector = SearchVector('text')
            for word in query_dict:
                que = SearchQuery(word)
                trend_temp = Trend.objects.annotate(qTitle=SearchRank(vectorTitle, que), qText=SearchRank(vector, que))
                for entry in trend_temp:
                    entry.rank = round(entry.qTitle * settings.factorTitle + entry.qText * settings.factorText, 4)
                    if entry.rank >= settings.filterGTE:
                        if dominantEssence == "direction":
                            entry.rank += settings.factorPage
                        result_dict['/direction/' + str(entry.id)] = {
                            'id': entry.id,
                            'rank': entry.rank,
                            'title': entry.title,
                            'titlePreview': None,
                            'type': 'direction'
                        }


        founded_content = ResultDictBuilder(result_dict)
        count_content = len(founded_content)
        return Response({
            "data": founded_content[offset:offset + 12],
            "count": count_content,
       })
