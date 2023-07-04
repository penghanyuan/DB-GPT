import json
import importlib
from pilot.prompts.prompt_new import PromptTemplate
from pilot.configs.config import Config
from pilot.scene.base import ChatScene
from pilot.scene.chat_dashboard.out_parser import ChatDashboardOutputParser, ChartItem
from pilot.common.schema import SeparatorStyle

CFG = Config()

PROMPT_SCENE_DEFINE = """You are a {dialect} data analysis expert, please provide a professional data analysis solution according to the following situations"""

_DEFAULT_TEMPLATE = """
According to the structure definition in the following tables:
{table_info}
Provide professional data analysis, use as few dimensions as possible, but no less than three, and no more than eight dimensions.
Used to support goal: {input}

Pay attention to the length of the output content of the analysis result, do not exceed 4000tokens
According to the characteristics of the analyzed data, choose the best one from the charts provided below to display，chart types:
{supported_chat_type}

Give {dialect} data analysis SQL, analysis title, display method and analytical thinking,respond in the following json format:
{response}
Do not use unprovided fields and do not use unprovided data in the where condition of sql.
Ensure the response is correct json and can be parsed by Python json.loads
"""

RESPONSE_FORMAT = [
    {
        "sql": "data analysis SQL",
        "title": "Data Analysis Title",
        "showcase": "What type of charts to show",
        "thoughts": "Current thinking and value of data analysis",
    }
]

PROMPT_SEP = SeparatorStyle.SINGLE.value

PROMPT_NEED_NEED_STREAM_OUT = False

prompt = PromptTemplate(
    template_scene=ChatScene.ChatDashboard.value(),
    input_variables=["input", "table_info", "dialect", "supported_chat_type"],
    response_format=json.dumps(RESPONSE_FORMAT, indent=4),
    template_define=PROMPT_SCENE_DEFINE,
    template=_DEFAULT_TEMPLATE,
    stream_out=PROMPT_NEED_NEED_STREAM_OUT,
    output_parser=ChatDashboardOutputParser(
        sep=PROMPT_SEP, is_stream_out=PROMPT_NEED_NEED_STREAM_OUT
    ),
)
CFG.prompt_templates.update({prompt.template_scene: prompt})
