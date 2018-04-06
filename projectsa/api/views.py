from .serializers import EditDistanceSerializer
from rest_framework.decorators import list_route
from drf_braces.mixins import MultipleSerializersViewMixin
from rest_framework.generics import GenericAPIView


from rest_framework.response import Response
from rest_framework import viewsets, status


class EditDistanceViewSet(viewsets.ViewSet,
                          MultipleSerializersViewMixin,
                          GenericAPIView):
    """ This class handles edit distance calculation."""

    @list_route(methods=['put'], url_path='find-edit-distance')
    def find_edit_distance(self, request):
        """This method calculate edit distance for the given string pairs"""
        serializer = self.get_serializer(
            data=request.data,
            serializer_class=EditDistanceSerializer)
        serializer.is_valid(raise_exception=True)
        s1 = serializer.data["first_string"]
        s2 = serializer.data["second_string"]
        if len(s1) > len(s2):
            s1, s2 = s2, s1

        distances = range(len(s1) + 1)
        for i2, c2 in enumerate(s2):
            distances_ = [i2 + 1]
            for i1, c1 in enumerate(s1):
                if c1 == c2:
                    distances_.append(distances[i1])
                else:
                    distances_.append(1 + min((distances[i1],
                                               distances[i1 + 1],
                                               distances_[-1])))
            distances = distances_

        ret = {'edit_distance': distances[-1]}
        return Response(ret)
