from django.conf import settings

from ldap3 import Server, Connection, ObjectDef, AttrDef, Reader, Writer, ALL
from account.models import FomoUser
from catalog.models import ShoppingCart

class ActiveDirectoryBackend(object):
    '''
    Authenticate against Active Directory
    '''
    def authenticate(self, username=None, password=None):
        active_directory = LDAP()
        ad_user = active_directory.authenticate(username, password)

        if ad_user != None:
            try:
                user = FomoUser.objects.get(username=ad_user.sAMAccountName)
            except FomoUser.DoesNotExist:
                user = FomoUser()
                user.username = ad_user.sAMAccountName
                user.first_name = ad_user.givenName
                user.last_name = ad_user.sn
                user.email = str(ad_user.userPrincipalName).replace('.local', '.us')
                user.is_staff = True
                user.save()
                cart = ShoppingCart(user=user)
                cart.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return FomoUser.objects.get(pk=user_id)
        except FomoUser.DoesNotExist:
            return None


class LDAP(object):
    server = Server(settings.AD_SERVER, get_info=ALL)
    conn = Connection(server, settings.AD_ADMIN_DN, settings.AD_ADMIN_PASS, auto_bind=True)

    def authenticate(self, username, password):
        # search for user in AD
        self.conn.search(
            'DC=familymusic,DC=local',
            '(sAMAccountName={})'.format(username),
            attributes=['userPrincipalName', 'sn', 'givenName', 'distinguishedName', 'sAMAccountName']
        )
        try:
            ad_user = self.conn.entries[0]
            Connection(self.server, str(ad_user.distinguishedName), password, auto_bind=True)
            print(ad_user)
        except:
            return None

        return ad_user
