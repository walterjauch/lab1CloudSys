# Deliverable 1.2

# Répartition des architectures

- Toniutti Lucas : AWS
- Truong David : SwitchEngine
- Pin Guillaume : Google
- Jauch Walter : Exoscale
- Debray Julien : Azure

# Application déployée

Pour le premier labo, nous proposons de déployer une application développée lors d’un précédent TP. L’application consiste en un OCR permettant de dessiner un chiffre sur un cadre de 20x20 pixels puis de laisser le programme deviner le chiffre.

## Front office

La partie front office est développée en HTML / CSS / JS. Elle permet plusieurs choses :

- L’utilisateur peut dessiner dans un cadre
- Un bouton permet d’entraîner l’OCR
- Un bouton permet de faire deviner le dessin à l’OCR

Le JS communique avec le BO via une API. On envoie une liste de coordonnées puis on reçoit un chiffre.

## Back office

Le partie back office est développée en Python. Elle est composée d’une API pour communiquer avec le FO, d’un algorithme permettant de deviner le chiffre dessiné ainsi que d’un algorithme permettant d’entraîner l’OCR.

Le BO communique avec le module de stockage afin de récupérer / ajouter des images d’entraînement.

## Storage

Les données que nous avons à stocker sont les images servant à l’OCR de reconnaître le chiffre à deviner.

**Lien vers le projet :** [https://githepia.hesge.ch/nikola.antonije/cloud-lab1](https://githepia.hesge.ch/nikola.antonije/cloud-lab1)

# Evaluation des architectures

|  | Prise en main | Documentation API | Coût |
| --- | --- | --- | --- |
| AWS | Prise en main relativement facile malgré quelques petits bugs durant le projet. | Prise en main relativement facile malgré quelques petits bugs durant le projet. | Aucune informations concernant les prix. |
| Google | Prise en main difficile au début, courbe d’apprentissage raide (sans expérience dans le domaine ou autre plateforme). | Documentation adaptée et complète pour la opérations sur VMs. | Très bas. Les 50$ de budget initial sont largement suffisants. |
| Exoscale | Prise en main simple et rapide on arrive a faire facilement des instance. | Documentation difficile à comprendre et difficile à la trouver.  | ~0.10 CHF/heure des machines qui sont lancé. |
| Azure | Prise en main assez facile une fois l’architecture comprise. Principe de devoir lié plusieurs interface assez intuitif. | Excellente documentation, très complète et avec beaucoup d’exemple. | ~0.12 USD/heure. L’hébergement de VM éteinte étant payant, il faut bien faire attention à supprimer les instances. |
| Switch | Il n’y pas de tutoriel pour guider une création de VM sur l’interface graphique.  | La documentation n’est pas toujours à jour. Il y a de la redondance au niveau des fonctionnalités proposées. | Coût dans le temps des adresses IP allouées. Communications avec un Object Storage hébergé sur une autre architecture génère des coûts supplémentaires. |

# Conclusion

Ce travail nous a permis d’aborder des aspects de déploiement d’application via le Cloud. Malgré quelques difficultés avec certaines infrastructures et le manque de connaissances théoriques, nous avons réussi à déployer notre application sur plusieurs architectures.

Nous avons trouvé enrichissant ce travail et nous permettra par la suite d’être plus à l’aise avec le déploiement de VM.