from flask import Blueprint, render_template, request
from website.models import Result


# create instance of Blueprint; 'sort' is the name
sort = Blueprint('sort', __name__)


@sort.route('/rate_high', methods=['GET', 'POST'])
def rate_high():
    city = Result.query.with_entities(Result.city).limit(1).scalar()
    page = request.args.get('page', 1, type=int)
    page_results = Result.query.order_by(Result.rating.desc())\
                                                .paginate(page=page, per_page=2)
    return render_template('rate_high.html', results=page_results, origin=city)


@sort.route('/rate_low', methods=['GET', 'POST'])
def rate_low():
    city = Result.query.with_entities(Result.city).limit(1).scalar()
    page = request.args.get('page', 1, type=int)
    page_results = Result.query.order_by(Result.rating.asc())\
                                                .paginate(page=page, per_page=2)
    return render_template('rate_low.html',
                           results=page_results,
                           origin=city)


@sort.route('/time_fast', methods=['GET', 'POST'])
def time_fast():
    city = Result.query.with_entities(Result.city).limit(1).scalar()
    page = request.args.get('page', 1, type=int)
    page_results = Result.query.order_by(Result.duration.asc())\
                                                .paginate(page=page, per_page=2)
    return render_template('time_fast.html',
                           results=page_results,
                           origin=city)


@sort.route('/time_slow', methods=['GET', 'POST'])
def time_slow():
    city = Result.query.with_entities(Result.city).limit(1).scalar()
    page = request.args.get('page', 1, type=int)
    page_results = Result.query.order_by(Result.duration.desc())\
                                                .paginate(page=page, per_page=2)
    return render_template('time_slow.html',
                           results=page_results,
                           origin=city)
