import bcrypt

from members.models import Member, State, Role

def create_member_data():
    pw1 = bcrypt.hashpw('asdf1234'.encode('utf-8'), bcrypt.gensalt())
    pw2 = bcrypt.hashpw('qwer1234'.encode('utf-8'), bcrypt.gensalt())
    Member.objects.create(id='20201641', name='정재헌', password=pw1, phone='01000000000', email='test1@gmail.com', state=State.ENROLLED, role=Role.STAFF, message='hi', image='image1')
    Member.objects.create(id='20231560', name='신현수', password=pw2, phone='01000000001', email='test2@gmail.com', state=State.ENROLLED, role=Role.STAFF, message='hello', image='image2')

    