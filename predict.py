from cog import BasePredictor, Input, Path, BaseModel
from typing import Optional
import shutil
import os

# On définit la structure des sorties pour que Weavy voit bien les "ports"
class RouterOutput(BaseModel):
    # Sorties pour la voie du HAUT (Switch OFF)
    text_output_top: Optional[str]
    image_output_top: Optional[Path]
    
    # Sorties pour la voie du BAS (Switch ON)
    text_output_bottom: Optional[str]
    image_output_bottom: Optional[Path]

class Predictor(BasePredictor):
    def setup(self):
        """Rien à charger au démarrage (pas de modèle lourd)"""
        pass

    def predict(
        self,
        switch_on: bool = Input(
            description="SWITCH: Si OFF (désactivé) -> Sortie HAUT. Si ON (activé) -> Sortie BAS.", 
            default=False
        ),
        text_input: str = Input(
            description="Entrée pour du TEXTE (Prompt)", 
            default=None
        ),
        image_input: Path = Input(
            description="Entrée pour une IMAGE", 
            default=None
        ),
    ) -> RouterOutput:
        
        # Initialisation des variables de sortie à None (Vide)
        t_top = None
        i_top = None
        t_bottom = None
        i_bottom = None

        # --- LOGIQUE DU ROUTER ---
        
        # Si Switch est ON (Vrai) -> On envoie vers le BAS
        if switch_on:
            if text_input:
                t_bottom = text_input
            if image_input:
                # On prépare le chemin de sortie pour l'image
                output_path = Path("output_bottom.png")
                shutil.copy(image_input, output_path)
                i_bottom = output_path
                
        # Si Switch est OFF (Faux) -> On envoie vers le HAUT
        else:
            if text_input:
                t_top = text_input
            if image_input:
                output_path = Path("output_top.png")
                shutil.copy(image_input, output_path)
                i_top = output_path

        # On retourne l'objet complet
        return RouterOutput(
            text_output_top=t_top,
            image_output_top=i_top,
            text_output_bottom=t_bottom,
            image_output_bottom=i_bottom
        )
