import os
from jinja2 import Environment, FileSystemLoader

def generate_template(app_name, TEMPLATES):
    env = Environment(
        loader=FileSystemLoader("app/templates"),
        block_start_string="[%", 
        block_end_string="%]", 
        variable_start_string="[[", 
        variable_end_string="]]",
        autoescape=False,
    )

    for template in TEMPLATES:
        name = template["name"]
        os.makedirs(f"generated/{ app_name }/templates/{template['name']}", exist_ok=True)
        template_file_list = env.get_template(f"list.html")
        template_file_detail = env.get_template(f"detail.html")
        template_file_form = env.get_template(f"form.html")
        template_file_delete = env.get_template(f"confirm_delete.html")
        html_list = template_file_list.render(name=name, app_name=app_name.lower(), tables_columns=template["tables_columns"])
        html_detail = template_file_detail.render(name=name, app_name=app_name.lower(), tables_columns=template["tables_columns"])
        html_form = template_file_form.render(name=name, app_name=app_name.lower())
        html_delete = template_file_delete.render(name=name, app_name=app_name.lower())

        with open(f"generated/{ app_name.lower() }/templates/{template['name']}/list.html", "w") as f:
            f.write(html_list)
        with open(f"generated/{ app_name.lower() }/templates/{template['name']}/detail.html", "w") as f:
            f.write(html_detail)
        with open(f"generated/{ app_name.lower() }/templates/{template['name']}/form.html", "w") as f:
            f.write(html_form)
        with open(f"generated/{ app_name.lower() }/templates/{template['name']}/confirm_delete.html", "w") as f:
            f.write(html_delete)