# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: 
# Collaborators (discussion):
# Time:

#Importing this for legacy code
import matplotlib.pylab as pylab
import re
import numpy as np

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    result = []
    for d in degs:
        result.append(pylab.polyfit(x,y,d))
    return result  


def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    error = (y - estimated)**2
    variance = (y - y.mean())**2
    return 1 - error.sum()/variance.sum()

def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models:
        predict_y = pylab.polyval(model,x)
        #Get type of model
        if len(model) <= 4:
            types_of_model = ["linear","quadratic","cubic"]
            model_type = types_of_model[len(model) - 2]
        else:
            model_type = f"{len(model)-1} degree"
        #make the title
        title = f"Years against degrees C with {model_type} model \n R2 = {round(r_squared(y,predict_y),5)}"
        #If model is linear get se_over_slope and add to title
        if len(model) == 2:
            title += f"\nStandard error to slope ratio = {round(se_over_slope(x,y,predict_y,model),5)}"
        #Draw two pairs of values
        pylab.figure()
        pylab.plot(x,y, "bo", x, predict_y, "-r")
        pylab.title(title)
        pylab.xlabel("Years")
        pylab.ylabel("Temperature in degrees C")
        pylab.show()
    

def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    result = []
    for year in years:
        total = 0
        for city in multi_cities:
            #Get sum of all mean temps for cities
            total += climate.get_yearly_temp(city, year).mean()
        #Add the mean for that year to result
        result.append(total/len(multi_cities))
    return pylab.array(result)


def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    result = []
    for i in range(len(y)):
        start_index = i - window_length + 1
        if start_index < 0:
            result.append(
                #Get mean from start of array till i
                pylab.array(y[:i+1]).mean()
            )
        else:
            result.append(
                #Get mean from start_index to i
                pylab.array(y[start_index:i+1]).mean()
            )
    return pylab.array(result)

def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    error = (y - estimated)**2
    mean_square_error = error.sum()/len(y)
    return mean_square_error**0.5
    

def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    result = []
    for year in years:
        city_temps = []
        national_temp = []
        for city in multi_cities:
            #Get a list of arrays, each array is all the daily temps of the year for each city
            city_temps.append(climate.get_yearly_temp(city, year))
        #turn the list of arrays into a numpy array
        city_temps = np.array(city_temps)
        #go over the 2d array and get an array of temperatures for that day, add the standard deviation to national_temp
        for day in range(len(city_temps[0])):
            daily_temps = city_temps[:,day]
            national_temp.append(pylab.array(daily_temps).mean())
        result.append(np.std(national_temp))
    return pylab.array(result)

def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model???s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models:
        predict_y = pylab.polyval(model,x)
        #Get type of model
        if len(model) <= 4:
            types_of_model = ["linear","quadratic","cubic"]
            model_type = types_of_model[len(model) - 2]
        else:
            model_type = f"{len(model)-1} degree"
        #make the title
        title = f"Years against degrees C with {model_type} model \n RMSE = {round(rmse(y,predict_y),5)}"
        #Draw two pairs of values
        pylab.figure()
        pylab.plot(x,y, "bo", x, predict_y, "-r")
        pylab.title(title)
        pylab.xlabel("Years")
        pylab.ylabel("Temperature in degrees C")
        pylab.show()

if __name__ == '__main__':

    all_temps = Climate("data.csv") 

    # Part A.4
    def new_york_daily_temps(Climate):
        """
        Takes in a instance of a climate object and plots model of a day's temperature's trend over training period.
        """
        #Get temperature for Jan 10th in New York
        city = "NEW YORK"
        month = 1
        day = 10
        new_york_temps = []
        #Make training interval into pylab.array() to use as x values
        #Only convert to array once nothing else is needed to be added (otherwise have to copy all array everytime)
        x = pylab.array(TRAINING_INTERVAL)
        for year in x:
            new_york_temps.append(
            Climate.get_daily_temp(city, month, day, year)
            )
        y = pylab.array(new_york_temps)
        model = generate_models(x, y, [1])
        evaluate_models_on_training(x, y, model)
    #Call new_york function
    new_york_daily_temps(all_temps)


    # Annual temperatures
    def new_york_annual_temps(Climate):
        """
        Takes in a instance of a climate object and plots model of a city's annual temperature trend over training period.
        """
        #Get temperature for Jan 10th in New York
        city = "NEW YORK"
        new_york_temps = []
        #Make training interval into pylab.array() to use as x values
        #Only convert to array once nothing else is needed to be added (otherwise have to copy all array everytime)
        x = pylab.array(TRAINING_INTERVAL)
        for year in x:
            #For every year get the mean temperature
            new_york_temps.append(
            Climate.get_yearly_temp(city, year).mean()
            )
        y = pylab.array(new_york_temps)
        model = generate_models(x, y, [1])
        evaluate_models_on_training(x, y, model)
    #Call new_york_annual_temps function
    new_york_annual_temps(all_temps)

    #Part B - national average temperatures
    def national_annual_temps(climate):
        """
        Takes in a instance of a climate object and plots model of all US city's annual temperature trend over training period.
        """
        #Get list of average temp for national cities over training interval period
        y = gen_cities_avg(climate, CITIES, TRAINING_INTERVAL)
        #Make training interval into pylab.array() to use as x values
        #Only convert to array once nothing else is needed to be added (otherwise have to copy all array everytime you add a value)
        x = pylab.array(TRAINING_INTERVAL)
        model = generate_models(x, y, [1])
        evaluate_models_on_training(x, y, model)
    #Call new_york_annual_temps function
    national_annual_temps(all_temps)

    # Part C
    def national_five_year_temps(climate):
        """
        Takes in a instance of a climate object and plots model of all US city's 5 year average of annual temperature trend over training period.
        """
        #Get list of average temp for national cities over training interval period
        city_temps = gen_cities_avg(climate, CITIES, TRAINING_INTERVAL)
        #Turn city_temps into 5 year moving average
        y = moving_average(city_temps,5)
        #Make training interval into pylab.array() to use as x values
        x = pylab.array(TRAINING_INTERVAL)
        model = generate_models(x, y, [1])
        evaluate_models_on_training(x, y, model)
    #Call new_york_annual_temps function
    national_five_year_temps(all_temps)

    # Part D.2
    def five_year_models(climate, degs):
        """
        Args:
            climate: instance of a Climate object
            degs: list of integers, specifying degrees of model tested to data
        Returns:
            a list of pylab arrays, where each array is a 1-d array of coefficients that minimizes the squared error of the fitting polynomial
        """
        #Get list of average temp for national cities over training interval period
        city_temps = gen_cities_avg(climate, CITIES, TRAINING_INTERVAL)
        #Turn city_temps into 5 year moving average
        y = moving_average(city_temps,5)
        #Make training interval into pylab.array() to use as x values
        x = pylab.array(TRAINING_INTERVAL)
        models = generate_models(x, y, degs)
        evaluate_models_on_training(x, y, models)
        return models
    #Call the function
    training_models = five_year_models(all_temps, [1,2,20])

    def five_year_predictions(climate, models):
        """
        Args:
            climate: instance of a Climate object
            models: a list of pylab arrays, each array is a 1-d array of coefficients that minimizes the squared error of the fitting polynomial, from training data, to be tested in testing data
        Returns:
            Models found
        """
        #Get list of average temp for national cities over training interval period
        city_temps = gen_cities_avg(climate, CITIES, TESTING_INTERVAL)
        #Turn city_temps into 5 year moving average
        y = moving_average(city_temps, 5)
        #Make training interval into pylab.array() to use as x values
        x = pylab.array(TESTING_INTERVAL)
        evaluate_models_on_testing(x,y,models)
    #Call the function
    five_year_predictions(all_temps, training_models)

    # Part E
    def model_extreme_temp(climate):
        """
        Args:
            climate: instance of a Climate object
            degs: list of integers, specifying degrees of model tested to data
        Returns:
            nothing
        """
        #Get list of average temp for national cities over training interval period
        city_temps = gen_std_devs(climate, CITIES, TRAINING_INTERVAL)
        #Turn city_temps into 5 year moving average
        y = moving_average(city_temps,5)
        #Make training interval into pylab.array() to use as x values
        x = pylab.array(TRAINING_INTERVAL)
        models = generate_models(x, y, [1])
        evaluate_models_on_training(x, y, models)
    #call the function
    model_extreme_temp(all_temps)