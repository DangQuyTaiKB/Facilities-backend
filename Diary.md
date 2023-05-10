## Téma:
## Vytvořte datové struktury pro definici areálu, budovy, patra a místnosti v budově, navažte na datové struktury uživatel a skupina umožňující definovat stupeň odpovědnosti za areál, budovu, místnost (např. velitel, správce, nájemce apod.

#### **1.týden po zadání projektu(léto)**
Vybrali jsme si téma číslo 2, jelikož vypadalo strukturově dost podobné již vypracovanému UG-> EASY WAY

#### **první týden semestru**
Zjišťujeme, že naše plány projekt udělat během prázdnin se rozplynuly jako ranní mlha, jediné co nás uklidňuje je, že to nebylo kvůli naší neschopnosti ale pouze vytíženosti (čti chronická lenost)
#### **1. týden po první hodině**
Díky ukázce z hodiny v rámci struktury UG začínáme tvarovat první modely/entity (zatím pouze na papír) a jejich základní schéma, co se týče vztahů mezi nimi. 
Snažíme se pochopit princip federace a resolverů

#### **2. týden**
Přenéšíme hotový diagramový model do Lucidchartu kvůli komplikovanosti údržby/editovatelnosti+prezentovatelnosti
Před prvním projektovým dnem ještě vytváříme dummy model pro apolo (prosím ať se před tím borcem z OKIS nic neposere)

#### **První projektový den**
Šlo to lépe než jsem čekal+máme zelenou na modely
  
#### **2 týdny po projektovém dni**
V rámci konzultace docházíme k názoru, že bude lepším řešením překopat princip architektury facilities, kdy v původním návrhu byly entitpy hierarchizky rozděleny v rámci tabulek area/budva/patro/místrnost. Tento model je ovšem poněkud nešťasný pro generalizaci, jelikož bude muset být překopán při každé potřebě přidat prostory, které zde nejsou zahrnuty nebo nějakou operaci, jenž nebude logická s touto architekturou. Z tohoto důvodu přecházíme na model "facilities" jako jediné tabulky a druhou tabulkou "facility_types" ve vztahu n:1. Takto budeme schopni v případě potřeby vytvořit nové typy facilit a operace můžeme provádět jaké chceme

#### **4 týdny po projektovém dni**
Začíná experimentace s Jupyterem a stjně rychle jako jsme začali, tak rychle jsme s tím skončili. Největším problémem bylo propsání z jupyteru do pgadminu do databáze (error byl hlášen v connection stringu, ale ten sedí). Přenášíme projekt zpět do vs code, což k našemu překvapení řeší většinu našich problémů s propsáním struktury databáze oproti Jupyteru.
Začínáme tvořit resolvery (čti topíme se na nich jako myši)-> buď požehnány uoishelpers

#### **2. projektový den**
Došly na kukačku nějaké návštěvnice z ciziny. Sdílíme naše útrapy s Jupyterem, ALE dostáváme jistotu, že už nebudeme měnit modely Juchůůů

#### **1 týden po 2. projektovém dnu**
Prolézáme GraphTypeDefinitions a definujeme své gql modely (datetime je prevít). Prvbí pokus o feeder
 #### **2. týden po 2. projektovém dnu**
 No feeder z ug je zbytečný overkill, chce to něco jednodušího(nakonec je to jednoduší a taky trochu na prasáka, ALE funguje to). V rámci nasoukání dat do pgadminu narážíme na problém, že do něj musíme nejdříve zanést uuid managera, jelikož je to cizí kontejner (bez konzultace by nebylo šance)

 #### **4. týden po 2. projektovém dnu**
 začínáme víc pracovat na resolverech+query->say hello+facility by id (neočekávané úspěchy)

 #### **3. projektový den**
 no nic moc, přes Vánoce místo projektu jsme řešili cukroví, takže místo query máme 10 kilo navíc, černé svědomí, ale fajnové zážitky

#### **začátek zkouškového**
Co si budeme, jsme pěkně v kýblu a možná ještě hůř a editor nikde. Tohle bude bolet a k tomu docker začíná trolit s compose up (lenoch si prostě změn jen tak pro srandu nevšimne a nechá tě hledat bug co už je vyřešený, strašné had)

#### **průběh zkouškového**
Editor se dal, ale řešíme hloupé bugy stylu description na usertable, apod. No prostě mamlasové

#### **poslední dny před odevzdání**
"A man of focus, commitment and sheer will" i takto by šly tyto dny shrnout+ dokumentace, VŠUDE dokumetace
 
#### **den před zkouškou**
Při dopisování těchto vět jsem si uvědomil, že ještě musím udělat docker image wish me luck
