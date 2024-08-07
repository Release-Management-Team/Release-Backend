from activities.models import Study, Project

def create_activity_data():
    study1 = Study.objects.create(name='두근두근 하스켈 클럽', president_id='20231560', goal='하스켈 정복', description='하스켈로 함수형 프로그래밍을 맛보아요')
    study2 = Study.objects.create(name='React로 나만의 웹페이지 만들기', president_id='20201641', goal='리액트를 공부하며 프론트엔드의 기초 함양', description='React와 자바스크립트를 통해 웹 프론트엔드의 기초를 공부합니다.')
    