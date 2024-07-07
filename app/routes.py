from flask import Blueprint, request, jsonify, send_file, render_template_string
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

    html_template = """
    <html>
    <head><title>{{ data.name }} - Monster Stat Block</title></head>
    <body>
        <h1>{{ data.name }}</h1>
        <p><strong>Type:</strong> {{ data.type }}</p>
        <p><strong>Alignment:</strong> {{ data.alignment }}</p>
        <p><strong>Armor Class:</strong> {{ data.armor_class }}</p>
        <p><strong>Hit Points:</strong> {{ data.hit_points }} ({{ data.hit_dice }})</p>
        <p><strong>Speed:</strong> Walk {{ data.speed.walk }} ft, Fly {{ data.speed.fly }} ft, Swim {{ data.speed.swim }} ft</p>
        <h2>Ability Scores</h2>
        <ul>
            <li><strong>Strength:</strong> {{ data.ability_scores.strength }}</li>
            <li><strong>Dexterity:</strong> {{ data.ability_scores.dexterity }}</li>
            <li><strong>Constitution:</strong> {{ data.ability_scores.constitution }}</li>
            <li><strong>Intelligence:</strong> {{ data.ability_scores.intelligence }}</li>
            <li><strong>Wisdom:</strong> {{ data.ability_scores.wisdom }}</li>
            <li><strong>Charisma:</strong> {{ data.ability_scores.charisma }}</li>
        </ul>
        <h2>Special Traits</h2>
        <ul>
            {% for trait in data.special_traits %}
                <li><strong>{{ trait.name }}:</strong> {{ trait.description }}</li>
            {% endfor %}
        </ul>
        <h2>Actions</h2>
        <ul>
            {% for action in data.actions %}
                <li><strong>{{ action.name }}:</strong> {{ action.description }}</li>
            {% endfor %}
        </ul>
        <h2>Legendary Actions</h2>
        <ul>
            {% for legendary_action in data.legendary_actions %}
                <li><strong>{{ legendary_action.name }}:</strong> {{ legendary_action.description }}</li>
            {% endfor %}
        </ul>
        <h2>Lair Actions</h2>
        <ul>
            {% for lair_action in data.lair_actions %}
                <li><strong>{{ lair_action.name }}:</strong> {{ lair_action.description }}</li>
            {% endfor %}
        </ul>
        <h2>Regional Effects</h2>
        <ul>
            {% for regional_effect in data.regional_effects %}
                <li><strong>{{ regional_effect.name }}:</strong> {{ regional_effect.description }}</li>
            {% endfor %}
        </ul>
    </body>
    </html>
    """
    rendered_html = render_template_string(html_template, data=data)

    pdf_output = io.BytesIO()
    pisa_status = pisa.CreatePDF(io.StringIO(rendered_html), dest=pdf_output)
    pdf_output.seek(0)

    if pisa_status.err:
        return jsonify({'error': 'Error generating PDF'}), 500

    return send_file(pdf_output, as_attachment=True, download_name='monster_stat_block.pdf', mimetype='application/pdf')
