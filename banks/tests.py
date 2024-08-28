# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Bank, Branch

class BankBranchViewsTestCase(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='testuser@example.com',
            first_name='Test',
            last_name='User'
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')
        
        # Create test bank and branch
        self.bank = Bank.objects.create(
            name='Test Bank',
            description='Test Bank Description',
            inst_num='12345',
            swift_code='TESTCODE',
            admin=self.user
        )
        
        self.branch = Branch.objects.create(
            name='Test Branch',
            transit_num='67890',
            address='123 Test St',
            email='branch@test.com',
            capacity=100,
            bank=self.bank
        )

    def test_index_view(self):
        response = self.client.get(reverse('banks:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Bank')

    def test_edit_branch_view(self):
        response = self.client.get(reverse('banks:Edit_branch', args=[self.branch.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit_branch')

        response = self.client.post(reverse('banks:Edit_branch', args=[self.branch.pk]), {
            'name': 'Updated Branch',
            'transit_num': '54321',
            'address': '456 Test Ave',
            'email': 'updatedbranch@test.com',
            'capacity': 200
        })
        self.branch.refresh_from_db()
        self.assertEqual(response.status_code, 200)  # Redirect status code
        self.assertEqual(self.branch.name, 'Updated Branch')
        self.assertEqual(self.branch.transit_num, '54321')

    def test_about_view(self):
        response = self.client.get(reverse('banks:about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'About')

    def test_accounts_view(self):
        response = self.client.get(reverse('banks:accounts'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'accounts')

    def test_view_user_data(self):
        response = self.client.get(reverse('banks:view'))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'testuser',
            'email': 'testuser@example.com',
            'pk': self.user.pk
        })

    def test_add_bank_view(self):
        response = self.client.get(reverse('banks:AddBank'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Add Bank')

        response = self.client.post(reverse('banks:AddBank'), {
            'name': 'New Bank',
            'description': 'New Bank Description',
            'inst_num': '67890',
            'swift_code': 'NEWCODE'
        })
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertTrue(Bank.objects.filter(name='New Bank').exists())

    def test_user_view(self):
        response = self.client.get(reverse('banks:user_view'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'user_view')

    def test_edit_user_view(self):
        response = self.client.get(reverse('banks:edit'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'edit')

        response = self.client.post(reverse('banks:edit'), {
            'id': self.user.pk,
            'uname': 'updateduser',
            'fname': 'Updated',
            'lname': 'User',
            'email': 'updateduser@example.com'
        })
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.email, 'updateduser@example.com')

    def test_add_branch_view(self):
        response = self.client.get(reverse('banks:addbranch'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Add Branch')

        response = self.client.post(reverse('banks:addbranch'), {
            'name': 'New Branch',
            'transit_num': '112233',
            'address': '789 New St',
            'email': 'newbranch@test.com',
            'capacity': 150,
            'bank_id': self.bank.pk
        })
        self.assertEqual(response.status_code, 200)  # Render view status code
        self.assertTrue(Branch.objects.filter(name='New Branch').exists())

    def test_addbranch_view(self):
        response = self.client.get(reverse('banks:Addbranch', args=[self.bank.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Add Branch')

    def test_details_view(self):
        response = self.client.get(reverse('banks:details', args=[self.bank.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Branch')

    def tearDown(self):
        # Clean up after tests
        self.user.delete()
        self.bank.delete()
        self.branch.delete()
