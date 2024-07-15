from src import Model,Field

if __name__ == '__main__':
    class PersonModel(Model):
        is_admin = Field.boolean(default=True)
        gpa = Field.number(default=4.5)
        last_name = Field.string(max_length=5)

    p1 = PersonModel(is_admin=False, gpa=4.5,
                     last_name="Smith", first_name="Mike")
    # try:
    
    final_obj = p1.validate().build()
    print(final_obj)