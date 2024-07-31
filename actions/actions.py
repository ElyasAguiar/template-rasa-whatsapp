# actions.py

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionConsultarProcesso(Action):

    def name(self) -> Text:
        return "action_consultar_processo"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        numero_processo = tracker.get_slot("numero_processo")

        # Aqui você pode adicionar a lógica para consultar o processo, por exemplo, chamando uma API.
        # Vamos usar um exemplo fictício:
        if numero_processo:
            status_processo = "Em andamento"  # Substitua pela lógica real de consulta
            dispatcher.utter_message(
                text=f"O status do processo {numero_processo} é: {status_processo}"
            )
        else:
            dispatcher.utter_message(
                text="Não consegui encontrar o número do processo. Você pode fornecer o número do processo?"
            )

        return []


class ActionDefaultFallback(Action):

    def name(self) -> Text:
        return "action_default_fallback"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(
            text="Desculpe, não entendi isso. Pode reformular sua pergunta?"
        )

        return []
