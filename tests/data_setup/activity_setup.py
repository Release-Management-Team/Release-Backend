from activities.models import Event, Study, StudyTag, Project
from datetime import datetime, timezone

from members.models import Member

def create_activity_data():
    event1 = Event.objects.create(
        name='개강총회',
        description='2024년 가을학기 개강을 맞아 개강총회를 개최합니다.',
        start_date=datetime(2024, 9, 2, 18, 0).astimezone(),
        end_date=datetime(2024, 9, 2, 19, 0).astimezone()
    )

    pl = StudyTag.objects.create(tag='프로그래밍언어')
    web = StudyTag.objects.create(tag='웹')
    frontend = StudyTag.objects.create(tag='프론트엔드')

    study1 = Study.objects.create(
        name='두근두근 하스켈 클럽', 
        leader_id='20231560',
        description='하스켈로 함수형 프로그래밍을 맛보아요'
    )
    study1.tags.add(pl)
    study1.members.add(Member.objects.get(id='20201641'))
    
    study2 = Study.objects.create(
        name='React로 나만의 웹페이지 만들기', 
        leader_id='20201641', 
        description='React와 자바스크립트를 통해 웹 프론트엔드의 기초를 공부합니다.'
    )
    study2.tags.add(web)
    study2.tags.add(frontend)

    