import json, random, math

class RandomObject(object):

    # Use the description value in the json, then reflect it into a formatter
    def describe(self, from_perspective=None):
        # Get the raw string and the list of keys for formatting
        desc_raw = getattr(self,'description')
        desc_values = list(getattr(self,x) for x in getattr(self,'description_keys'))
        # This line mutates the string with a description_mutator
        pre_mutation = desc_raw.format(*desc_values)
        return pre_mutation.format(*desc_values)

    # randomize a field in the json and apply it to this RandomObject
    def randomize(self, type_to_randomize):
        type_value = self.parameter_types[type_to_randomize]
        # Get a random number between 0 and (len-1). This fixes an Ob1 error
        random_val = random.randint(0,len(type_value)-1)
        result = type_value[random_val]
        # Use reflection to set the type attribute to the result
        setattr(self,type_to_randomize,result)

    # Read the Json and add the types and keys to the RandomObject appropriately
    def read_in_random_parameters(reader):
        all_random_parameters = json.load(open("RandomValues.txt",'r'))
        reader_name = reader.__class__.__name__.lower()
        reader.parameter_types = {k:v for (k,v) in all_random_parameters[reader_name].items() if not 'description_keys' in k}
        reader.description_keys = all_random_parameters[reader_name]['description_keys']

    def sqrt_random(minimum,maximum,scale):
        absolute_max = round(math.sqrt(scale))
        random_value = round(math.sqrt(random.randint(1,scale)))
        return int(max(random_value - (absolute_max-maximum), minimum))

    def __init__(self):
        self.read_in_random_parameters()
        for params in self.parameter_types:
            self.randomize(params)
