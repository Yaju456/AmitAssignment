from mrjob.job import MRJob

class CoffeeSalesCounter(MRJob):

    def mapper(self, _, line):
        # Split the line based on commas
        parts = line.strip().split(", ")
        
        # Ensure the line contains the expected number of elements
        if len(parts) == 7:
            coffee_type = parts[0]
            try:
                money = float(parts[2])  # Extract the money field and convert it to float
                yield coffee_type, money  # Yield coffee type with the associated money value
            except ValueError:
                pass  # Skip lines with invalid money values

    def reducer(self, coffee_type, money_values):
        # Sum all the money amounts for each coffee type
        total_sales = sum(money_values)
        yield coffee_type, round(total_sales, 2)

if __name__ == '__main__':
    # Run the job with the default runner (uses LocalRunner by default)
    CoffeeSalesCounter.run()
