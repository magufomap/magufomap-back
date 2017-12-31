from rest_framework import routers

from .change_requests import views as changerequests_viewsets
from .comments import views as comments_viewsets
from .poims import views as poims_viewsets
from .ratings import views as ratings_viewsets
from .tags import views as tags_viewsets
from .users import views as users_viewsets

router = routers.DefaultRouter()
# router.register(r"current-user/mypoimswithchangerequests", views.POIMsWithChangeRequestsViewSet)
# router.register(r"current-user", views.ProfileViewSet, "User")
router.register(r"change-requests", changerequests_viewsets.ChangeRequestViewSet)
router.register(r"comments", comments_viewsets.CommentViewSet)
router.register(r"poims", poims_viewsets.POIMViewSet)
router.register(r"ratings", ratings_viewsets.RatingViewSet)
router.register(r"tags", tags_viewsets.TagViewSet)
router.register(r"users", users_viewsets.UserViewSet)
