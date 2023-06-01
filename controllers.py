"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, redirect, URL, Field
from py4web.utils.form import Form, FormStyleBulma
from py4web.utils.url_signer import URLSigner

from .models import get_user_email
from . common import db, session, T, cache, auth, signed_url

url_signer = URLSigner(session)

@action('index')
@action.uses(db, auth.user, 'index.html')
def index():
    products = db(db.listing).select().as_list()
    return dict(products=products)


@action('add', method = ["GET", "POST"])
@action.uses(db, auth.user, 'add.html')
def add():
    form = Form(db.listing, csrf_session = session, formstyle = FormStyleBulma)
    if form.accepted:
        redirect(URL('index'))
    return dict(form = form)

@action('home', method=["GET", "POST"])
@action.uses(db, auth.user, 'index.html')
def home():
    redirect(URL('default', 'index'))


@action('description/<listing_id:int>', method = ["GET", "POST"])
@action.uses(db, auth.user, 'description.html')
def description(listing_id = None):
    assert listing_id is not None

    rows = db(db.listing.id == listing_id).select()

    return dict(rows = rows)


# This is an example only, to be used as inspiration for your code to increment the bird count.
# Note that the bird_id parameter ...
#@action('inc/<bird_id:int>') # the :int means: please convert this to an int.
#@action.uses(db, auth.user, url_signer.verify())
# ... has to match the bird_id parameter of the Python function here.
#def inc(bird_id=None):
#    assert bird_id is not None

#    b = db.bird[bird_id]
#    new_count = b.n_sighting + 1
#    b.update_record(n_sighting=new_count)
#    redirect(URL('index'))

#@action('edit/<bird_id:int>', method=["GET", "POST"])
#@action.uses('edit.html', db, auth.user)
#def edit(bird_id=None):
#    b = db.bird[bird_id]
 #   if get_user_email() != b.user_email:
 #       redirect(URL('index'))
        
 #   if b is None:
 #       redirect(URL('index'))
    
 #   form = Form(
 #       db.bird,
 #       record=b,
 #       deletable=False,
 #       formstyle=FormStyleBulma,
 #       csrf_session=session
 #       )
    
#    if form.accepted:
#        redirect(URL('index'))
#    return dict(form=form)


