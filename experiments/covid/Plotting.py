class Plotting():
    def __init__(self, h_weights =[], h_age =[], h_sex =[], h_morb =[], d_weights =[], d_age =[], d_sex =[], d_morb =[]
    ) -> None:

        self.h_weights = h_weights,
        self.h_age = h_age,
        self.h_sex = h_sex,
        self.h_morb = h_morb,
        self.d_weights = d_weights,
        self.d_age = d_age,
        self.d_sex = d_sex,
        self.d_morb = d_morb,

    def add_hosp(sex, age, weight, morb) -> None:
        h_weights = []
        h_age = []
        h_sex = []
        h_morb = []
        h_weights.append(weight)
        h_sex.append(sex)
        h_age.append(age)
        h_morb.append(morb)
        print(h_morb)

    def add_dead(self,sex, age, weight, morb):

        self.d_weights.append(weight)
        self.d_sex.append(sex)
        self.d_age.append(age)
        self.d_morb.append(morb)

