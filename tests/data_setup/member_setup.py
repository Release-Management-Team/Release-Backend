
from members.models import Member, State, Role
from utils.encryption import hashpw

def create_member_data():
    pw0 = hashpw('asdf1234')
    pw1 = hashpw('asdf5678')
    pw2 = hashpw('qwer1234')
    pw3 = hashpw('qwer5678')
    pw4 = hashpw('zcxv1234')
    pw5 = hashpw('zxcv5678')
    Member.objects.create(id='20201641', name='정재헌', password=pw0, phone='01000000000', email='test0@gmail.com', state=State.ENROLLED,   role=Role.STAFF,    message='hi',       image='image0')
    Member.objects.create(id='20231560', name='신현수', password=pw1, phone='01000000001', email='test1@gmail.com', state=State.ENROLLED,   role=Role.STAFF,    message='hello',    image='image1')
    Member.objects.create(id='20211547', name='신지원', password=pw2, phone='01000000002', email='test2@gmail.com', state=State.ABSENCE,    role=Role.MEMBER,   message='spam',     image='image2')
    Member.objects.create(id='20201576', name='김현섭', password=pw3, phone='01000000003', email='test3@gmail.com', state=State.ENROLLED,   role=Role.MEMBER,   message='egg',      image='image3')
    Member.objects.create(id='20231592', name='이호준', password=pw4, phone='01000000004', email='test4@gmail.com', state=State.ENROLLED,   role=Role.MEMBER,   message='cheese',   image='image4')
    Member.objects.create(id='20140000', name='릴리즈', password=pw5, phone='01000000005', email='test5@gmail.com', state=State.GRADUATED,  role=Role.MEMBER,   message='kimchi',   image='image5')

    