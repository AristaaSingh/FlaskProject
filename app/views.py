from flask import render_template, redirect, url_for, flash, request
from app import app, db
from app.models import Assessment
from app.forms import AssessmentForm
from datetime import datetime
from sqlalchemy import func


# home page displays all assessment from database
@app.route('/')
def home():
    assessments = Assessment.query.all()
    return render_template('home.html', assessments=assessments)


# Add Assessment page: form for adding new assessments
# while also validating form data
@app.route('/add', methods=['GET', 'POST'])
def add_assessment():
    form = AssessmentForm()
    if form.validate_on_submit():
        existing_assessment = Assessment.query.filter(
            func.lower(Assessment.title) == func.lower(form.title.data),
            func.lower(Assessment.module_code) == func.lower(form.module_code.data)
        ).first()
        if existing_assessment:
            flash("This Title and Module Code already exists.", 'warning')
            return render_template('add_assessment.html', form=form)
        new_assessment = Assessment(
            title=form.title.data,
            module_code=form.module_code.data,
            deadline_date=form.deadline_date.data,
            description=form.description.data,
            is_complete=form.is_complete.data
        )
        db.session.add(new_assessment)
        db.session.commit()
        flash('Assessment added successfully!', 'success')
        return redirect(url_for('home'))
    else:
        print("Form is not valid")
        print(form.errors)
    return render_template('add_assessment.html', form=form)


# Edit Assessment page: form but with existing data that can be edited
@app.route('/edit/<int:assessment_id>', methods=['GET', 'POST'])
def edit_assessment(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    form = AssessmentForm(obj=assessment)
    if form.validate_on_submit():
        assessment.title = form.title.data
        assessment.module_code = form.module_code.data
        assessment.deadline_date = form.deadline_date.data
        assessment.description = form.description.data
        assessment.is_complete = form.is_complete.data
        db.session.commit()
        flash('Assessment updated successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('edit_assessment.html', form=form,
                           assessment=assessment)


# route for toggling completion status
@app.route('/complete/<int:assessment_id>', methods=['GET', 'POST'])
def complete_assessments(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    if request.method == 'POST':
        assessment.is_complete = not assessment.is_complete
        db.session.commit()
        if assessment.is_complete:
            flash('Assessment marked as complete!', 'success')
        else:
            flash('Assessment marked as incomplete!', 'success')
        return redirect(url_for('home'))
    return render_template('complete_assessments.html', assessment=assessment)


# Complete Assessments: displays assessments with status is_complete=True
@app.route('/completed')
def view_completed():
    completed_assessments = Assessment.query.filter_by(is_complete=True).all()
    return render_template('complete_assessments.html',
                           assessments=completed_assessments)


# Incomplete Assessments: displays assessments with status is_complete=False
@app.route('/incomplete')
def view_incomplete():
    incomplete_assess = Assessment.query.filter_by(is_complete=False).all()
    return render_template('incomplete_assessments.html',
                           assessments=incomplete_assess)


# route for removing assessment from database
@app.route('/delete/<int:assessment_id>', methods=['POST'])
def delete_assessment(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    db.session.delete(assessment)
    db.session.commit()
    flash('Assessment deleted successfully!', 'success')
    return redirect(url_for('home'))
