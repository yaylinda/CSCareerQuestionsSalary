import csv
import praw
from praw.models import MoreComments

column_names = [
    'Education', 
    'Prior Experience', 
    'Company/Industry', 
    'Title', 
    'Tenure length', 
    'Location', 
    'Salary', 
    'Stock and/or recurring bonuses', 
    'Total comp'
]

def parse_comments():

    print("Parsing comments...")

    reddit = praw.Reddit(
        user_agent='Comment Extraction (by /u/yaylindadev)',
        client_id='2q7spXD1h2mIbQ',
        client_secret="TI_YtXJmu5aoz8uptNYv9eYqo8g")

    data = []

    comment_ids = ['e0bd43x', 'e0bd43v', 'e0bd43r']

    for comment_id in comment_ids:

        comment = reddit.comment(id=comment_id)
        comment.refresh()

        for reply in comment.replies.list():

            if (type(reply) is not MoreComments) and (reply.parent() == comment_id):
                print('------------------------------')
                reply_body = reply.body.lower()
                print(reply_body)

                datum = {}
                for column_name in column_names:
                    print('\tnow searching for ' + column_name)
                    locator_str = column_name.lower() + ':'
                    
                    if reply_body.find(locator_str) != -1:
                        value = reply_body.split(locator_str)[1].split('\n')[0]
                        datum[column_name] = value
                        print('\t\tfound value: ' + value)
                    else:
                        print('\t\tdid not found value')
                        datum[column_name] = 'N/A'

                data.append(datum)

    return data


def write_to_csv(data):

    print("Writing to csv file...")

    csv_file = open('data.csv', 'w')
    csv_writer = csv.writer(csv_file, delimiter=',')
    csv_writer.writerow(column_names)
    
    for datum in data:
        csv_writer.writerow([
            datum[column_names[0]], 
            datum[column_names[1]], 
            datum[column_names[2]], 
            datum[column_names[3]], 
            datum[column_names[4]], 
            datum[column_names[5]], 
            datum[column_names[6]],
            datum[column_names[7]],
            datum[column_names[8]]
        ])

    csv_file.close()

def main():
    data = parse_comments()
    write_to_csv(data)

if __name__ == "__main__":
    main()
