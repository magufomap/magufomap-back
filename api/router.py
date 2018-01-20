from rest_framework import routers

from . import views

router = routers.DefaultRouter()
# router.register(r"current-user/mypoimswithchangerequests", views.POIMsWithChangeRequestsViewSet)
# router.register(r"current-user", views.ProfileViewSet, "User")
router.register(r"change-requests", views.ChangeRequestViewSet)
router.register(r"comments", views.CommentViewSet)
router.register(r"poims", views.POIMViewSet)
router.register(r"poim-images", views.POIMImageViewSet)
router.register(r"ratings", views.RatingViewSet)
router.register(r"tags", views.TagViewSet)
router.register(r"users", views.UserViewSet)
