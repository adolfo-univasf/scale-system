from .models import Program, ProgramTime
from datetime import date

def template_program(template: Program, date:date):
    #template = Program.objects.get(pk=7)
    program = Program()
    program.name = template.name
    program.date = date
    program.transmission = template.transmission
    program.room = template.room
    program.presential = template.presential
    program.iscription = template.iscription
    program.description = template.description
    program.save()
    template_times = ProgramTime.objects.filter(program = template)
    program_times = []
    for tt in template_times:
        pt = ProgramTime()
        pt.program = program
        pt.function = tt.function
        pt.lookup = tt.lookup
        pt.desc = tt.desc
        pt.time = tt.time
        pt.save()
        program_times.append(pt)
    return program#, program_times