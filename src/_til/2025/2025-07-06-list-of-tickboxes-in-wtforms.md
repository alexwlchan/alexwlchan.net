---
layout: til
title: Show a list of checkboxes in a WTForms form
summary: Subclass `SelectMultipleField` and override the `widget` and `option_widget` fields.
date: 2025-07-06 17:55:56 +01:00
tags:
  - python
---
I was working on a Flask app, which had a [web form](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms) using WTForms.
I wanted one of the form fields to be a list of items, from which the user could select one or more.

The basic functionality isn't tricky to write -- here's an example, using a [`SelectMultipleField`](https://wtforms.readthedocs.io/en/2.3.x/fields/#wtforms.fields.SelectMultipleField) to keep the list of options:

```python
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SubmitField


class MyForm(FlaskForm):
    colours = SelectMultipleField(
        "What colours do you like?",
        choices=["red", "orange", "yellow", "green", "blue", "indigo", "violet"],
    )
    submit = SubmitField("submit!")


app = Flask(__name__)
app.config["SECRET_KEY"] = "you-will-never-guess"


@app.route("/", methods=["GET", "POST"])
def homepage():
    form = MyForm()

    if form.validate_on_submit():
        print(f"The user likes {form.colours.data}")

    return f"""
        <form action="" method="post">
            {form.hidden_tag()}
            {form.colours(style="list-style-type: none;")}
            {form.submit}
        </form>
    """
```

This renders as an HTML [`<select>` element][select] with the [`multiple` attribute][multiple].
It technically works, but this is a somewhat unusual form control -- I'm not sure how many people would realise, for example, that you can shift-click to select multiple options.
(If you tap on this control in Safari on iOS, you see [a list of checkboxes](/images/2025/multiple-select-on-ios.jpeg).)

{%
  picture
  filename="multiple-select.png"
  width="263"
  class="screenshot"
  alt="A form with a single inset area with a list of four colours, one of which is highlighted blue, and a submit button."
%}

I wanted to render this as a list of checkboxes, and this is quite straightforward.
You can subclass `SelectMultipleField` and change a couple of the widgets:

```python
from wtforms import SelectMultipleField
from wtforms.widgets import CheckboxInput, ListWidget


class SelectMultipleCheckboxesField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()
```

and use this in the form instead of `SelectMultipleField`, and now you get a list of checkboxes:

{%
  picture
  filename="multiple-checkboxes.png"
  width="360"
  class="screenshot"
  alt="A form with a list of seven checkboxes, one per colour, and a submit button."
%}

These checkboxes work exactly as you'd expect, and get the nice validation behaviour and so on from WTForms.
Although I could certainly create a simple control by creating individual form fields, in some case it's convenient to have a list that WTForms renders for me.

[select]: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/select
[multiple]: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/multiple
