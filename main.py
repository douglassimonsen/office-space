import requests
import json
from pprint import pprint
import base64
import utilities
env  = json.load(open('env.json'))


def get_data():
    s = requests.session()
    access_code = s.post(
        "https://main.spaceiq.com/login",
        data=env['creds']
    ).json()['accessToken']
    s.headers = {
        "Content-Type": "application/json"
    }
    s.cookies['graphql_endpoint-main.spaceiq.com'] = 'https://api.spaceiq.com'
    s.cookies['access_token-main.spaceiq.com'] = access_code
    s.headers['authorization'] = 'Bearer ' + access_code
    return s.post(
        'https://api.spaceiq.com/queries?floorWithSpaceAssignments',
        json={
            "query":"\n  query floorWithSpaceAssignments($id:ID!, $assignmentPlanId: ID!) {\n    viewer {\n      viewFilters {\n        name\n        objectType\n        filters {\n          key\n          value\n          visible\n          displayName\n        }\n      }\n    }\n    node(id: $id) {\n      ... on Floor {\n        id\n        spaces(assignmentPlanId: $assignmentPlanId) {\n          ...fce06f2b0f3b64242909ebf8d15d2690c\n        }\n      }\n    }\n  }\n\n\n    fragment fce06f2b0f3b64242909ebf8d15d2690c on Space {\n      id\n      w\n      x\n      y\n      code\n      externalId\n      name\n      comment\n      density\n      measurements\n      capacity\n      status\n      spaceType(assignmentPlanId: $assignmentPlanId) {\n        ...f6036ab7a12174c78b9e9fbe0d20bea92\n      }\n      usageType(assignmentPlanId: $assignmentPlanId) {\n        name\n      }\n      workplaceGroup {\n        id,\n        name,\n        color\n      }\n      spaceAssignment(assignmentPlanId: $assignmentPlanId) {\n        externalId\n        sourceAssignmentPlanId\n        employee {\n          id\n          name\n          phone\n          employmentType\n          startDate\n          endDate\n          note\n          role\n          assets {\n            url(style: \"thumbnail\")\n          }\n          dept {\n            id\n            name\n          }\n          team {\n            id\n            name\n          }\n          workplaceGroup {\n            id,\n            name,\n            color\n          }\n        }\n        sharedEmployees {\n          id\n          name\n          role\n          workplaceGroup {\n            id,\n            name,\n            color\n          }\n          assets {\n            url(style: \"thumbnail\")\n          }\n          dept {\n            id\n            name\n          }\n          team {\n            id\n            name\n          }\n        }\n        department {\n          id\n          name\n          color\n        }\n        team {\n          id\n          name\n          color\n        }\n        neighborhood {\n          id\n          name\n          color\n        }\n      }\n    }\n  \n\n    fragment f6036ab7a12174c78b9e9fbe0d20bea92 on SpaceType {\n      id\n      name\n      interactivity\n      interactivityType\n      displayName\n      hidden\n    }\n  ",
            "variables": env['floorSeats']
        }

    ).json(), s


def seat_list(data):
    return [
        {
            "id": x['id'],
            "w": x['w'],
            'x': x['x'],
            'y': x['y'],
            'code': x['code'],
            'displayName': x['spaceType']['displayName'],
        } 
        for x in data['data']['node']['spaces']
    ]


def get_bookings(seat_ids, s):
    bookings = s.post(
        'https://api.spaceiq.com/queries?currentBookings',
        json={
            "query":"\n  query objectDetails($ids:[ID!]!, $fromDate: String) {\n    nodes(ids: $ids) {\n      ...fc3dd6f0cb27e40febbd3afd17f5232a8\n      ...fcee5b1e58099413a8b0f012abd2f5c6d\n    }\n  }\n\n\n    fragment fc3dd6f0cb27e40febbd3afd17f5232a8 on Space {\n      id\n      x\n      y\n      w\n      name\n      externalId\n      legacyId\n      code\n      density\n      measurements\n      capacity\n      comment\n      assets {\n        url(style: \"thumbnail\")\n        fullSizeUrl: url(style: \"half\")\n      }\n      tags {\n        id\n        name\n      }\n      workplaceGroup {\n        id\n        color\n        name\n      }\n      spaceType {\n        ...f950cbef6ef0f47a89edd554ca19c4414\n      }\n      usageType {\n        name\n        displayName\n      }\n      spaceAssignment {\n        department {\n          id\n          name\n          color\n        }\n        team {\n          id\n          name\n          color\n        }\n        employee {\n          ...f3d15a73506184c8f9b1860909413dcfe\n        }\n        sharedEmployees {\n          id\n          name\n          assets { url(style: \"thumbnail\") }\n          dept { id name }\n          team { id name }\n        }\n        neighborhood {\n          id\n          name\n          color\n          floor {\n            id\n            name\n            code\n            building {\n              code\n            }\n          }\n        }\n        device {\n          id\n          location\n          deviceCatalogId\n          badgeReaderIdentifier\n          deviceType { displayName }\n        }\n      }\n      floor {\n        ...f86e1910838b14b60a74f015f2373eba6\n      }\n      bookings(fromDate: $fromDate) {\n        id\n        startDate\n        endDate\n        autoReleasedAt\n        checkedIn\n        passedHealthCheck\n        bookingSchedule {\n          effectiveEndDate\n          effectiveStartDate\n          recurrencePattern\n        }\n        healthCheck {\n          disabled\n          locationHeathCheckGroup { id }\n        }\n        employee {\n          id\n          name\n          email\n          assets {\n            id\n            url\n          }\n          dept {\n            id\n            name\n            color\n          }\n          department {\n            id\n            name\n            color\n          }\n          team {\n            id\n            name\n          }\n        }\n        space {\n          id\n        }\n      }\n      calendar {\n        id\n        calendarName\n      }\n      sensors {\n        externalId\n        name\n      }\n    }\n  \n\n    fragment f950cbef6ef0f47a89edd554ca19c4414 on SpaceType {\n      id\n      name\n      interactivity\n      interactivityType\n      displayName\n      hidden\n    }\n  \n\n    fragment f3d15a73506184c8f9b1860909413dcfe on Employee {\n      id\n      externalId\n      costCenter { name }\n      name\n      title\n      employmentType\n      manager { name }\n      doNotCountAsUnallocated\n      isRemote\n      noDeskNeeded\n      email\n      role\n      startDate\n      endDate\n      phone\n      note\n      badge\n      extAttributes\n      assets {\n        url(style: \"thumbnail\")\n        fullSizeUrl: url(style: \"half\")\n      }\n      dept {\n        id\n        name\n        color\n      }\n      team {\n        id\n        name\n        color\n      }\n      tags {\n        id\n        name\n      }\n      departmentAdmins {\n        department {\n          id\n          name\n          colors\n        }\n      }\n      locationAdmins {\n        floorPlan {\n          id\n        }\n      }\n      neighborhoods {\n        id\n        name\n        color\n        floor {\n          id\n          name\n          code\n          building {\n            code\n          }\n        }\n      }\n      workplaceGroups {\n        id\n        color\n        name\n      }\n    }\n  \n\n    fragment f86e1910838b14b60a74f015f2373eba6 on Floor {\n      id\n      code\n      hidden\n      building {\n        code\n        timezone\n      }\n    }\n  \n\n    fragment fcee5b1e58099413a8b0f012abd2f5c6d on Employee {\n      ...f3d15a73506184c8f9b1860909413dcfe\n      spaceAssignment {\n        neighborhood {\n          id\n          name\n          color\n          floor {\n            id\n            name\n          }\n        }\n        space {\n          id\n          x\n          y\n          w\n          name\n          code\n          measurements\n          externalId\n          spaceType {\n            ...f950cbef6ef0f47a89edd554ca19c4414\n          }\n          usageType {\n            name\n            displayName\n          }\n          floor {\n            ...f86e1910838b14b60a74f015f2373eba6\n          }\n          tags {\n            id\n            name\n          }\n          sensors {\n            externalId\n            name\n          }\n        }\n      }\n    }\n  ",
            "variables":{
                "ids": seat_ids,
                "fromDate":"2022-04-27T05:00:00Z"
            }
        }
    ).json()
    # json.dump(bookings, open('bookings.json', 'w'), indent=4)
    return bookings


def update_dimension(table, data):
    data = data['filters']
    with utilities.get_conn() as conn:
        cursor = conn.cursor()
        for d in data:
            cursor.execute(
                f"insert into spaceiq.{table} (idx, name) values (%(value)s, %(displayName)s) on conflict do nothing", 
                d
            )
        conn.commit()


def update_seats(data):
    with utilities.get_conn() as conn:
        cursor = conn.cursor()
        for d in data:
            update_single_dimension("space_types", d['spaceType'], cursor)
            d['spaceType'] = d['spaceType']['id']
            cursor.execute(
                "insert into spaceiq.spaces values (%(id)s, %(spaceType)s, %(w)s, %(x)s, %(y)s, %(name)s) on conflict do nothing",
                d
            )
        conn.commit()


def update_single_dimension(table, data, cursor, columns=['id', 'name']):
    columns = ", ".join(f"%({x})s" for x in columns)
    cursor.execute(
        f"insert into spaceiq.{table} values ({columns}) on conflict do nothing", 
        data
    )


def update_booking_schedule(data, cursor):
    cursor.execute("""
    insert into spaceiq.booking_schedules (employee, space, start_dt, end_dt, schedule_type) 
    values (%(employee)s, %(space)s, %(effectiveStartDate)s, %(effectiveEndDate)s, %(recurrencePattern)s)
    on conflict do nothing
    returning idx
    """, data)
    ret = cursor.fetchone()
    if ret is None:
        cursor.execute("""select idx from spaceiq.booking_schedules
        where employee = %(employee)s
        and space = %(space)s
        and start_dt = %(effectiveStartDate)s
        and end_dt = %(effectiveEndDate)s
        and schedule_type = %(recurrencePattern)s
        """, data)
        return cursor.fetchone()[0]
    else:
        return ret[0]


def parse_bookings(bookings):
    with utilities.get_conn() as conn:
        cursor = conn.cursor()
        for d in bookings:
            for b in d['bookings']:
                update_single_dimension("departments", b['employee']['department'], cursor)
                for c in ['department', 'dept']:
                    b['employee'][c] = b['employee'][c]['id']
                update_single_dimension("employees", b['employee'], cursor, columns=['id', 'name', 'email', 'dept', 'department'])
                for c in ['employee', 'space']:
                    b[c] = b[c]['id']
                if b['bookingSchedule'] is not None:
                    b['bookingSchedule']['employee'] = b['employee']
                    b['bookingSchedule']['space'] = b['space']
                    b['bookingSchedule'] = update_booking_schedule(b['bookingSchedule'], cursor)
                update_single_dimension("bookings", b, cursor, columns=['id', 'employee', 'startDate', 'endDate', 'passedHealthCheck', 'checkedIn', 'autoReleasedAt', 'bookingSchedule', 'space'])
        conn.commit()


def main():
    # data, session = get_data()
    data = json.load(open("data.json"))
    dimensions = data['data']['viewer']['viewFilters']
    update_dimension('regions', dimensions[1])
    update_seats(data['data']['node']['spaces'])
    # json.dump(data, open("data.json", "w"), indent=4)
    # seats = seat_list(data)
    # get_bookings([s['id'] for s in seats], session)
    data = json.load(open('bookings.json'))['data']['nodes']
    parse_bookings(data)


if __name__ == '__main__':
    main()