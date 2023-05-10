import cloudconvert
# Import time module
import time

class CloudConvert:

    def __init__(self):
        cloudconvert.configure(
            api_key="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiMTIyY2YxNGZjZGY2MDQ4ZDBmYzVmOGVmZmM5MjU4YTMwYWFjZDUyZTlhZDgzMDViZGRlN2Y2MmNlMzBkNTc5MmJjNWEwNTZiMWI4NDczZWEiLCJpYXQiOjE2NDY2ODI2MDcuNzE3MzkyLCJuYmYiOjE2NDY2ODI2MDcuNzE3Mzk0LCJleHAiOjQ4MDIzNTYyMDcuNzA1Mzg0LCJzdWIiOiI1NjU0NTg4NiIsInNjb3BlcyI6WyJ1c2VyLnJlYWQiLCJ1c2VyLndyaXRlIiwidGFzay5yZWFkIiwidGFzay53cml0ZSIsIndlYmhvb2sucmVhZCIsIndlYmhvb2sud3JpdGUiLCJwcmVzZXQucmVhZCIsInByZXNldC53cml0ZSJdfQ.bkhlI2xEhk5KwAJq4rvK6J3cjecwf_BstfnBDA6-qCeccCgLQ6BqxWDNgRJo2-kxiyIrkVpBOg72WIOmWqa0APjzT6XjwEufsivGhwbisZVMX_JnnmTubY8oosc4m9_3cegny7fP4dRzMcHvMtHMR2MPMSl2yRvvwszvGz_oKEcCsesGxMERan4pdWvpTVJO6Bn_fLRA6g7PQvd_5V20wWwLswiDq41tYtYkRcX9aiO9bK7cfUkXSp-1x6MgcPn4qYacWTFtvIbHQ6J_ZCQOIppQ9ZxU9IH7WJpE4yyA9qnhCCo-XySFO241NeIyiN4cV7JGL_0xSro9KssrOqFMx7XcTtBZD_8UM7llDdjhfYRMEsZ2g6y9N2p00mCHQ12tRg1p5b4dOULkIXdxMb8L0At1GbR-ibPrpcqfZiQ8m8cmFQjmT0ycCzFebtrQ56cxJTBnlMiQVFLX7kvIpI2BuzyTWx1jHpToQwWYBNHevx4XhGiMyjK38u3rzoVVvEMNbZcRkID8Gi8zc7EYD5l-KIqi4KVO31vVUbagy7Ci_RLQ9cZEK4mCg-BOd5GPaGugWhiq2rJrKRyQqH_5rBax0LYE-mYqXinyNNiNeXP4jH9LGyYPMvMX1nuttM8fT73UIna5R8AyagJda2Nns_NOFzzF4OHeH3EvUuziJ2-a2Qo",
            sandbox=False)

    @staticmethod
    def pdf2xslx(input='', output=''):
        # record start time
        start = time.time()
        print('converting -->', input)

        # Define the conversion process
        job = cloudconvert.Job.create(payload={
             "tasks": {
                 'import-my-file': {
                      'operation': 'import/upload',
                 },
                 'convert-my-file': {
                     'operation': 'convert',
                     'input': 'import-my-file',
                     'input_format': 'pdf',
                     'output_format': 'xlsx',
                 },
                 'export-my-file': {
                     'operation': 'export/url',
                     'input': 'convert-my-file'
                 }
             }
         })

        upload_task_id = job['tasks'][0]['id']
        upload_task = cloudconvert.Task.find(id=upload_task_id)
        convert_task_id = job['tasks'][1]['id']
        print('Uploading File...')
        cloudconvert.Task.upload(file_name=input, task=upload_task)
        print("Uploading done in",
              (time.time() - start), "s")
        print('Converting File...')
        cloudconvert.Task.wait(id=convert_task_id)
        print("Conversion done in",
              (time.time() - start), "s")
        # cloudconvert.Task.wait(id=convert_task)
        export_url_task_id = job['tasks'][2]['id']
        print('Downloading File')
        res = cloudconvert.Task.wait(id=export_url_task_id)
        file = res.get("result").get("files")[0]
        res = cloudconvert.download(filename=output, url=file['url'])
        # record end time
        end = time.time()

        # print the difference between start
        # and end time in milli. secs
        print('data saved at: ', output)
        print("The time of execution of above program is :",
              (end - start) * 10 ** 3, "ms")
