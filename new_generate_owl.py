from owlready2 import *

# Create ontology (saved locally as GeoTutor.owl)
onto = get_ontology("http://geotutor.yorksj.ac.uk/onto#")

with onto:
    # Shape hierarchy
    class Shape(Thing):
        pass

    class Triangle(Shape):
        pass

    class Square(Shape):
        pass

    class Rectangle(Shape):
        pass

    # Data properties for shapes
    class hasBase(DataProperty, FunctionalProperty):
        domain = [Triangle]
        range = [float]

    class hasHeight(DataProperty, FunctionalProperty):
        domain = [Triangle]
        range = [float]

    class hasSide(DataProperty, FunctionalProperty):
        domain = [Square]
        range = [float]

    class hasLength(DataProperty, FunctionalProperty):
        domain = [Rectangle]
        range = [float]

    class hasWidth(DataProperty, FunctionalProperty):
        domain = [Rectangle]
        range = [float]

    class hasArea(DataProperty, FunctionalProperty):
        domain = [Shape]
        range = [float]

    class explains(DataProperty, FunctionalProperty):
        domain = [Shape]
        range = [str]

    # ITS student model
    class Student(Thing):
        pass

    class Resource(Thing):
        pass

    class studies(ObjectProperty):
        domain = [Student]
        range = [Resource]

    class hasMastery(DataProperty, FunctionalProperty):
        domain = [Student]
        range = [float]  # 0.0–1.0

    class hasDifficultyLevel(DataProperty, FunctionalProperty):
        domain = [Resource]
        range = [str]  # "easy", "medium", "hard"

    class requiresPrerequisite(ObjectProperty):
        domain = [Resource]
        range = [Resource]

    # Make the three shape classes disjoint
    AllDisjoint([Triangle, Square, Rectangle])

    # MAGIC: also treat shapes as resources (so you see arrows to Resource)
    Triangle.is_a.append(Resource)
    Square.is_a.append(Resource)
    Rectangle.is_a.append(Resource)

    # SWRL rules for area
    Imp().set_as_rule(
        """Triangle(?t), hasBase(?t, ?b), hasHeight(?t, ?h),
           multiply(?temp, ?b, ?h), divide(?a, ?temp, 2) ->
           hasArea(?t, ?a), explains(?t, "Area = ½ × base × height")"""
    )

    Imp().set_as_rule(
        """Square(?s), hasSide(?s, ?side),
           multiply(?a, ?side, ?side) ->
           hasArea(?s, ?a), explains(?s, "Area = side²")"""
    )

    Imp().set_as_rule(
        """Rectangle(?r), hasLength(?r, ?l), hasWidth(?r, ?w),
           multiply(?a, ?l, ?w) ->
           hasArea(?r, ?a), explains(?r, "Area = length × width")"""
    )

    # Demo individuals
    demo_student = Student("DemoStudent")
    demo_student.hasMastery = 0.65

    tri_resource = Resource("Triangle_Easy")
    tri_resource.hasDifficultyLevel = "easy"
    demo_student.studies.append(tri_resource)

    sq_resource = Resource("Square_Medium")
    sq_resource.hasDifficultyLevel = "medium"
    demo_student.studies.append(sq_resource)

    t1 = Triangle("DemoTriangle")
    t1.hasBase = 10.0
    t1.hasHeight = 6.0

# Save ontology to local file used by your app / Protégé
onto.save(file="GeoTutor.owl", format="rdfxml")
print("GeoTutor.owl successfully generated/extended.")