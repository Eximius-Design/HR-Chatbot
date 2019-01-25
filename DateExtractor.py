
import parsedatetime as pdt

class DateExtractor:

    def parse_date(text):
        cal = pdt.Calendar()
        try:
            Number_of_Dates = len(cal.nlp(text))
            dates = []
            if Number_of_Dates == 2:
                result = cal.nlp(text)[0]
                dates.append(str(result[0].date()))
                result = cal.nlp(text)[1]
                dates.append(str(result[0].date()))
            elif Number_of_Dates == 1:
                result = cal.nlp(text)[0]
                dates.append(str(result[0].date()))

            return dates
        except TypeError:

            return None


date=DateExtractor.parse_date("i will not be ")
print(date)
