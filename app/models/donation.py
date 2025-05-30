from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.charity_project import ProjectDonation


class Donation(ProjectDonation):
    user_id = Column(Integer, ForeignKey("user.id"))
    comment = Column(Text)
