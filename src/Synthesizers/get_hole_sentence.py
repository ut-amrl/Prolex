from dsl import *
from Synthesizers.synthesizer_v0 import *

def get_hole_context(sketch, top_level, hole_stmnt_pos, if_stmnt_hole_pos=0):
    #Get statement that we want to fill context for
    center_stmnt = sketch
    for pos in hole_stmnt_pos:
        center_stmnt = center_stmnt.statements[pos]

    holes_before_center_stmnt = 0
    center_stmnt_seen = False
    sentence = ""

    for stmnt in top_level.statements:
        if type(stmnt) is Goto:
            # Get NL Info
            temp_sentence, temp_holes = stmnt.nl()

            # Add to sentence
            sentence = temp_sentence

            #Recurse on sub statements
            temp_holes_before_center, temp_center_stmnt_seen, temp_sentence = get_hole_context(sketch, stmnt, hole_stmnt_pos, if_stmnt_hole_pos)

            #Update meta params
            if not center_stmnt_seen:
                holes_before_center_stmnt = holes_before_center_stmnt + temp_holes_before_center
                center_stmnt_seen = temp_center_stmnt_seen

            #Add to sentence
            sentence = sentence + temp_sentence

        if type(stmnt) is Scan:
            #Get NL Info
            temp_sentence, temp_holes = stmnt.nl()

            #Check if this is the statement we want context for
            if stmnt == center_stmnt:
                center_stmnt_seen = True
            elif not center_stmnt_seen:
                holes_before_center_stmnt = holes_before_center_stmnt + temp_holes

            if temp_sentence != "":
                sentence = sentence + ". Then, " + temp_sentence

        if type(stmnt) is If:
            #Get NL Info
            temp_sentence, temp_holes = stmnt.nl()

            # Check if this is the statement we want context for
            if stmnt == center_stmnt:
                center_stmnt_seen = True

                #Add holes before within If stmnt context
                holes_before_center_stmnt = holes_before_center_stmnt + if_stmnt_hole_pos
            elif not center_stmnt_seen:
                holes_before_center_stmnt = holes_before_center_stmnt + temp_holes

            if temp_sentence != "":
                sentence = sentence + ". Then, " + temp_sentence

            # Recurse on sub statements
            temp_holes_before_center, temp_center_stmnt_seen, temp_sentence = get_hole_context(sketch, stmnt,
                                                                                               hole_stmnt_pos, if_stmnt_hole_pos)

            # Update meta params
            if not center_stmnt_seen:
                holes_before_center_stmnt = holes_before_center_stmnt + temp_holes_before_center
                center_stmnt_seen = temp_center_stmnt_seen

            # Add to sentence
            if temp_sentence != "":
                sentence = sentence + ". Then, " + temp_sentence

        if type(stmnt) is Foreach_obj:
            # Recurse on sub statements
            temp_holes_before_center, temp_center_stmnt_seen, temp_sentence = get_hole_context(sketch, stmnt,
                                                                                               hole_stmnt_pos, if_stmnt_hole_pos)

            # Update meta params
            if not center_stmnt_seen:
                holes_before_center_stmnt = holes_before_center_stmnt + temp_holes_before_center
                center_stmnt_seen = temp_center_stmnt_seen

            # Add to sentence
            sentence = sentence + temp_sentence

        if type(stmnt) is Act:
            # Get NL Info
            temp_sentence, temp_holes = stmnt.nl()

            # Check if this is the statement we want context for
            if stmnt == center_stmnt:
                center_stmnt_seen = True
            elif not center_stmnt_seen:
                holes_before_center_stmnt = holes_before_center_stmnt + temp_holes

            sentence = sentence + temp_sentence

    return holes_before_center_stmnt, center_stmnt_seen, sentence
