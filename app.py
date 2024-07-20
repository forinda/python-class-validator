from src import Model,Field

if __name__ == '__main__':
    class PersonModel(Model):
        is_admin = Field.boolean(default=True)
        gpa = Field.number(default=4.5)
        last_name = Field.string(min_length=1)

    p1 = PersonModel(is_admin=False, gpa=4.5,
                     first_name="Mike",last_name="3")
    try:
    
        final_obj = p1.validate().build()
        print(final_obj)
    except Exception as e:
        print(e.errors)