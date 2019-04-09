# coding=utf-8
import datetime
from nmp_broker.plugins.loadleveler.filters.long_time_operation_job_filter import \
    get_datetime_data, \
    create_filter


# TODO: repeat is evil
def create_job(
        job_id="id_no",
        owner="owner",
        job_class="job_class",
        queue_date=datetime.datetime.utcnow(),
        status="R",
        priority=100
):
    return {
        "props": [
            {
                "id": "llq.id",
                "data": job_id,
                "text": job_id,
                "value": job_id
            },
            {
                "id": "llq.owner",
                "data": owner,
                "text": owner,
                "value": owner
            },
            {
                "id": "llq.class",
                "data": job_class,
                "text": job_class,
                "value": job_class
            },
            {
                "id": "llq.job_script",
                "data": "llq.job_script" + job_id,
                "text": "llq.job_script" + job_id,
                "value": "llq.job_script" + job_id
            },
            {
                "id": "llq.status" + job_id,
                "data": status,
                "text": status,
                "value": status
            },
            {
                "id": "llq.queue_date",
                "data": queue_date.strftime("%Y-%m-%d %H:%M:%S"),  # 2017-04-21 07:08:43
                "text": queue_date.strftime("%m/%d %H:%M"),  # "04/21 07:08",
                "value": queue_date.strftime("%a %b %d %H:%M:%S %Y"),  # "Fri Apr 21 07:08:43 2017"
            },
            {
                "id": "llq.priority",
                "data": priority,
                "text": priority,
                "value": priority
            }
        ]
    }


def test_get_datetime_data():
    d = datetime.datetime.strptime("2017-03-04 05:06:08", "%Y-%m-%d %H:%M:%S")
    job = create_job(queue_date=d)
    queue_date = get_datetime_data(job, "llq.queue_date")
    assert queue_date == d


def test_create_filter(monkeypatch):

    class PatchedDatetime(datetime.datetime):
        pass

    def mock_now(tz=None):
        return datetime.datetime(2017, 3, 4, 5, 6, 8)

    monkeypatch.setattr(PatchedDatetime, 'utcnow', mock_now)
    datetime.datetime = PatchedDatetime
    a_filter = create_filter()

    job_items = [
        create_job(
            owner="nwp",
            queue_date=datetime.datetime(2017, 3, 4, 1, 6, 8)),
        create_job(
            owner="nwp",
            queue_date=datetime.datetime(2017, 3, 4, 2, 6, 8)),
        create_job(
            owner="nwp",
            queue_date=datetime.datetime(2017, 3, 2, 5, 6, 8)),
        create_job(
            owner="wangdp",
            queue_date=datetime.datetime(2017, 3, 1, 5, 6, 8))
    ]
    target_job_items = a_filter['filter'].filter(job_items)
    assert len(target_job_items) == 1
