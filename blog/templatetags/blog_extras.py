from django import template
from django.utils import timezone

register = template.Library()

# Création de la classe pour gérer la balise de template


class GetPostedAtDisplayNode(template.Node):
    def __init__(self, time):
        self.time = template.Variable(time)

    def render(self, context):
        # Résolution du contexte pour obtenir la valeur du temps
        time = self.time.resolve(context)
        now = timezone.now()

        # Calcul de la différence de temps
        diff = now - time
        minutes = diff.total_seconds() / 60
        hours = minutes / 60

        # Rendu dynamique en fonction du temps écoulé
        if minutes < 60:
            return f"Posté il y a {int(minutes)} minutes"
        elif hours < 24:
            return f"Posté il y a {int(hours)} heures"
        else:
            return time.strftime("Posté à %H:%M %d %b %y")

# Fonction pour enregistrer la balise


def get_posted_at_display(parser, token):
    try:
        tag_name, time = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires a single argument" % token.contents.split()[0])
    return GetPostedAtDisplayNode(time)


# Enregistrement de la balise dans la bibliothèque de templates
register.tag('get_posted_at_display', get_posted_at_display)
