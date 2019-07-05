import csv

silver_plans = list()
solvable_rate_areas = set()
zip_codes_rate_areas = dict()


def process_slcsp_file():
    with open('slcsp.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        print('zipcode,rate')
        for row in reader:
            print(f"{row['zipcode']},{get_rate(row['zipcode'])}")


def get_rate(zipcode):
    rate_areas = zip_codes_rate_areas[zipcode]
    if len(rate_areas) != 1:
        return ''

    rate_area = list(rate_areas)[0]
    if rate_area not in solvable_rate_areas:
        return ''

    silver_plans_for_rate_area = get_silver_plans_by_rate_area(rate_area)

    rates = set(map(lambda plan: plan['rate'], silver_plans_for_rate_area))

    if len(rates) > 1:
        return get_slcsp((rates))
    else:
        return ''


def get_silver_plans_by_rate_area(rate_area):
    return list(filter(lambda silver_plan: silver_plan['rate_area'] == rate_area, silver_plans))


def get_slcsp(rates):
    return '{0:.2f}'.format(float(sorted(rates)[1]))


def load_silver_plans():
    with open('plans.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        next(reader)
        for row in reader:
            if row['metal_level'] == 'Silver':
                silver_plans.append({
                    'id': row['plan_id'],
                    'rate_area': (row['state'], row['rate_area']),
                    'rate': row['rate'],
                })
                solvable_rate_areas.add((row['state'], row['rate_area']))


def load_zipcodes_rate_areas():
    with open('zips.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['zipcode'] not in zip_codes_rate_areas.keys():
                zip_codes_rate_areas[row['zipcode']] = set()
            zip_codes_rate_areas[row['zipcode']].add(
                (row['state'], row['rate_area']))


if __name__ == "__main__":
    load_silver_plans()
    load_zipcodes_rate_areas()
    process_slcsp_file()
