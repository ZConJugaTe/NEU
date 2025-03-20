
```
library
├─ books
│  ├─ admin.py
│  ├─ apps.py
│  ├─ forms.py
│  ├─ migrations
│  │  ├─ 0001_initial.py
│  │  ├─ 0002_auto_20241118_1840.py
│  │  ├─ 0003_auto_20241124_2149.py
│  │  ├─ 0004_alter_book_id_alter_loan_id.py
│  │  ├─ 0005_passwordresetrequest.py
│  │  ├─ __init__.py
│  │  └─ __pycache__
│  │     ├─ 0001_initial.cpython-310.pyc
│  │     ├─ 0002_auto_20241118_1840.cpython-310.pyc
│  │     ├─ 0003_auto_20241124_2149.cpython-310.pyc
│  │     ├─ 0004_alter_book_id_alter_loan_id.cpython-310.pyc
│  │     ├─ 0005_author_alter_book_author.cpython-310.pyc
│  │     ├─ 0005_category_book_category.cpython-310.pyc
│  │     ├─ 0005_passwordresetrequest.cpython-310.pyc
│  │     ├─ 0006_alter_book_category.cpython-310.pyc
│  │     ├─ 0007_remove_category_in_stock_remove_category_total_books_and_more.cpython-310.pyc
│  │     ├─ 0008_remove_book_category_delete_category.cpython-310.pyc
│  │     └─ __init__.cpython-310.pyc
│  ├─ models.py
│  ├─ templates
│  │  ├─ books
│  │  │  ├─ base.html
│  │  │  ├─ book_batch_upload.html
│  │  │  ├─ book_confirm_delete.html
│  │  │  ├─ book_detail.html
│  │  │  ├─ book_form.html
│  │  │  ├─ book_list.html
│  │  │  ├─ change_password.html
│  │  │  ├─ forget_password.html
│  │  │  ├─ loaned_books.html
│  │  │  ├─ loan_form.html
│  │  │  ├─ login.html
│  │  │  ├─ register.html
│  │  │  ├─ user_request.html
│  │  │  └─ view_users.html
│  │  └─ home.html
│  ├─ tests.py
│  ├─ urls.py
│  ├─ views.py
│  ├─ __init__.py
│  └─ __pycache__
│     ├─ admin.cpython-310.pyc
│     ├─ apps.cpython-310.pyc
│     ├─ forms.cpython-310.pyc
│     ├─ models.cpython-310.pyc
│     ├─ urls.cpython-310.pyc
│     ├─ views.cpython-310.pyc
│     └─ __init__.cpython-310.pyc
├─ db.sqlite3
├─ er_diagram.dot
├─ library
│  ├─ asgi.py
│  ├─ settings.py
│  ├─ urls.py
│  ├─ wsgi.py
│  ├─ __init__.py
│  └─ __pycache__
│     ├─ settings.cpython-310.pyc
│     ├─ urls.cpython-310.pyc
│     ├─ wsgi.cpython-310.pyc
│     └─ __init__.cpython-310.pyc
├─ manage.py
├─ prompt.txt
├─ README.md
└─ staticfiles
   └─ admin
      ├─ css
      │  ├─ autocomplete.css
      │  ├─ base.css
      │  ├─ changelists.css
      │  ├─ dashboard.css
      │  ├─ fonts.css
      │  ├─ forms.css
      │  ├─ login.css
      │  ├─ responsive.css
      │  ├─ responsive_rtl.css
      │  ├─ rtl.css
      │  ├─ vendor
      │  │  └─ select2
      │  │     ├─ LICENSE-SELECT2.md
      │  │     ├─ select2.css
      │  │     └─ select2.min.css
      │  └─ widgets.css
      ├─ fonts
      │  ├─ LICENSE.txt
      │  ├─ README.txt
      │  ├─ Roboto-Bold-webfont.woff
      │  ├─ Roboto-Light-webfont.woff
      │  └─ Roboto-Regular-webfont.woff
      ├─ img
      │  ├─ calendar-icons.svg
      │  ├─ gis
      │  │  ├─ move_vertex_off.svg
      │  │  └─ move_vertex_on.svg
      │  ├─ hya.jpeg
      │  ├─ icon-addlink.svg
      │  ├─ icon-alert.svg
      │  ├─ icon-calendar.svg
      │  ├─ icon-changelink.svg
      │  ├─ icon-clock.svg
      │  ├─ icon-deletelink.svg
      │  ├─ icon-no.svg
      │  ├─ icon-unknown-alt.svg
      │  ├─ icon-unknown.svg
      │  ├─ icon-viewlink.svg
      │  ├─ icon-yes.svg
      │  ├─ inline-delete.svg
      │  ├─ LICENSE
      │  ├─ README.txt
      │  ├─ search.svg
      │  ├─ selector-icons.svg
      │  ├─ sorting-icons.svg
      │  ├─ tooltag-add.svg
      │  └─ tooltag-arrowright.svg
      └─ js
         ├─ actions.js
         ├─ actions.min.js
         ├─ admin
         │  ├─ DateTimeShortcuts.js
         │  └─ RelatedObjectLookups.js
         ├─ autocomplete.js
         ├─ calendar.js
         ├─ cancel.js
         ├─ change_form.js
         ├─ collapse.js
         ├─ collapse.min.js
         ├─ core.js
         ├─ inlines.js
         ├─ inlines.min.js
         ├─ jquery.init.js
         ├─ popup_response.js
         ├─ prepopulate.js
         ├─ prepopulate.min.js
         ├─ prepopulate_init.js
         ├─ SelectBox.js
         ├─ SelectFilter2.js
         ├─ timeparse.js
         ├─ urlify.js
         └─ vendor
            ├─ jquery
            │  ├─ jquery.js
            │  ├─ jquery.min.js
            │  └─ LICENSE.txt
            ├─ select2
            │  ├─ i18n
            │  │  ├─ ar.js
            │  │  ├─ az.js
            │  │  ├─ bg.js
            │  │  ├─ ca.js
            │  │  ├─ cs.js
            │  │  ├─ da.js
            │  │  ├─ de.js
            │  │  ├─ el.js
            │  │  ├─ en.js
            │  │  ├─ es.js
            │  │  ├─ et.js
            │  │  ├─ eu.js
            │  │  ├─ fa.js
            │  │  ├─ fi.js
            │  │  ├─ fr.js
            │  │  ├─ gl.js
            │  │  ├─ he.js
            │  │  ├─ hi.js
            │  │  ├─ hr.js
            │  │  ├─ hu.js
            │  │  ├─ id.js
            │  │  ├─ is.js
            │  │  ├─ it.js
            │  │  ├─ ja.js
            │  │  ├─ km.js
            │  │  ├─ ko.js
            │  │  ├─ lt.js
            │  │  ├─ lv.js
            │  │  ├─ mk.js
            │  │  ├─ ms.js
            │  │  ├─ nb.js
            │  │  ├─ nl.js
            │  │  ├─ pl.js
            │  │  ├─ pt-BR.js
            │  │  ├─ pt.js
            │  │  ├─ ro.js
            │  │  ├─ ru.js
            │  │  ├─ sk.js
            │  │  ├─ sr-Cyrl.js
            │  │  ├─ sr.js
            │  │  ├─ sv.js
            │  │  ├─ th.js
            │  │  ├─ tr.js
            │  │  ├─ uk.js
            │  │  ├─ vi.js
            │  │  ├─ zh-CN.js
            │  │  └─ zh-TW.js
            │  ├─ LICENSE.md
            │  ├─ select2.full.js
            │  └─ select2.full.min.js
            └─ xregexp
               ├─ LICENSE.txt
               ├─ xregexp.js
               └─ xregexp.min.js

```