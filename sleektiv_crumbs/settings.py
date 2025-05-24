from sleektiv.settings import TEMPLATES

TEMPLATES[0]["OPTIONS"]["context_processors"].append(
    "sleektiv_crumbs.context_processors.breadcrumbs",
)
