from flask import Blueprint, request, jsonify, send_file, render_template, url_for
from jsonschema import validate, ValidationError
from xhtml2pdf import pisa
import io

main = Blueprint('main', __name__)

monster_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "type": {"type": "string"},
        "alignment": {"type": "string"},
        "armor_class": {"type": "integer"},
        "hit_points": {"type": "integer"},
        "hit_dice": {"type": "string"},
        "speed": {
            "type": "object",
            "properties": {
                "walk": {"type": "integer"},
                "fly": {"type": "integer"},
                "swim": {"type": "integer"}
            },
            "required": ["walk"]
        },
        "ability_scores": {
            "type": "object",
            "properties": {
                "strength": {"type": "integer"},
                "dexterity": {"type": "integer"},
                "constitution": {"type": "integer"},
                "intelligence": {"type": "integer"},
                "wisdom": {"type": "integer"},
                "charisma": {"type": "integer"}
            },
            "required": ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]
        },
        "saving_throws": {
            "type": "object",
            "properties": {
                "strength": {"type": "integer"},
                "dexterity": {"type": "integer"},
                "constitution": {"type": "integer"},
                "intelligence": {"type": "integer"},
                "wisdom": {"type": "integer"},
                "charisma": {"type": "integer"}
            }
        },
        "skills": {
            "type": "object",
            "properties": {
                "perception": {"type": "integer"},
                "stealth": {"type": "integer"}
            }
        },
        "damage_resistances": {"type": "array", "items": {"type": "string"}},
        "damage_immunities": {"type": "array", "items": {"type": "string"}},
        "damage_vulnerabilities": {"type": "array", "items": {"type": "string"}},
        "condition_immunities": {"type": "array", "items": {"type": "string"}},
        "senses": {
            "type": "object",
            "properties": {
                "blindsight": {"type": "integer"},
                "darkvision": {"type": "integer"},
                "passive_perception": {"type": "integer"}
            }
        },
        "languages": {"type": "array", "items": {"type": "string"}},
        "challenge_rating": {"type": "integer"},
        "special_traits": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "description": {"type": "string"}
                },
                "required": ["name", "description"]
            }
        },
        "actions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "description": {"type": "string"}
                },
                "required": ["name", "description"]
            }
        },
        "legendary_actions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "description": {"type": "string"}
                },
                "required": ["name", "description"]
            }
        },
        "reactions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "description": {"type": "string"}
                },
                "required": ["name", "description"]
            }
        },
        "lair_actions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "description": {"type": "string"}
                },
                "required": ["name", "description"]
            }
        },
        "regional_effects": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "description": {"type": "string"}
                },
                "required": ["name", "description"]
            }
        }
    },
    "required": ["name", "type", "alignment", "armor_class", "hit_points", "hit_dice", "speed", "ability_scores", "challenge_rating"]
}

@main.route('/api/confirm-monster', methods=['POST'])
def confirm_monster():
    data = request.json
    try:
        validate(instance=data, schema=monster_schema)
    except ValidationError as e:
        return jsonify({"error": e.message}), 400

    rendered_html = render_template('template.html', data=data)

    pdf_output = io.BytesIO()
    pisa_status = pisa.CreatePDF(io.StringIO(rendered_html), dest=pdf_output)
    pdf_output.seek(0)

    if pisa_status.err:
        return jsonify({'error': 'Error generating PDF'}), 500

    return send_file(pdf_output, as_attachment=True, download_name='monster_stat_block.pdf', mimetype='application/pdf')
