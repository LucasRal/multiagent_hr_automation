```mermaid
flowchart TD
    A[Analyse Profil] -->|Success| B[Préparation Interview]
    B -->|Feedback reçu| C[Synthèse Finale]
    A -->|Erreur| E[Fin]
    B -->|En attente| D[Attente Feedback]
    C -->|Terminé| E[Fin]
```