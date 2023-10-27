from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from course.models import Course, Lesson, Subscription
from course.paginators import CoursePaginator, LessonPaginator
from course.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from permissions import IsOwner, IsModerator


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CoursePaginator

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [IsOwner | IsModerator | IsAdminUser]
        elif self.action == 'create':
            permission_classes = [IsAdminUser]
        elif self.action == 'destroy':
            permission_classes = [IsOwner | IsAdminUser]
        elif self.action == 'update':
            permission_classes = [IsOwner | IsModerator | IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated | IsAdminUser]


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = LessonPaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated | IsOwner | IsModerator | IsAdminUser]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated | IsOwner | IsModerator | IsAdminUser]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated | IsOwner | IsAdminUser]


class SubscriptionCourseCreateAPIView(generics.CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        course_id = kwargs.get('course_id')
        course = Course.objects.get(pk=course_id)

        if Subscription.objects.filter(user=request.user, course=course).exists():
            return Response({'detail': 'Вы уже подписаны на данный курс!'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data={'user': request.user.id, 'course': course.id})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({'detail': 'Подписка на данный курс выполнена успешно!'}, status=status.HTTP_201_CREATED)


class SubscriptionCourseDestroyAPIView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        course_id = self.kwargs.get('course_id')
        course = Course.objects.get(pk=course_id)
        return Subscription.objects.get(user=self.request.user, course=course)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'detail': 'Вы успешно отписались от данного курса!'}, status=status.HTTP_200_OK)
