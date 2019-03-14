2019-03-14
LT:
** Pokyciai Django serveryje: Pridetas funkcionalumas redaguoti daug su daug rysius 5versijos kompiuteriuose. **
* Laikinos atminties leidzia keisti tik tipa. Seriala, dydi ir dazni neleis nes juos turi imti per klientine programa.
    Issaugojama paspaudus issaugojimo mygtuka.
* Procesoriuose Gamintoja, Modeli, standartini dazni, maksimalu dazni, fizini ir logini branduoliu kieki leidzia redaguoti.
    Redaguojamas procesorius keicia procesoriaus irasa tik viename kompiuteryje o ne visuose kuriuose sis procesorius pasikartoja.
    Fizinis ir loginis branduoliu kiekis yra leidziamas ivesti tik sveikas skaicius.
    Issaugojama paspaudus issaugojimo mygtuka.
* Vaizdo plokste Gamintoja ir vaizdo plokstes pavadinima leidzia redaguoti.
    Redaguojama vaizdo plokste keicia vaizdo plokstes irasa tik viename kompiuteryje o ne visuose kuriuose si vaizdo plokste pasikartoja.
    Issaugojama paspaudus issaugojimo mygtuka.
* Draivu(HDD/SSD) redaguoti per computer_edit_v5 puslapi neleis. Vietoj to yra mygtukas "Edit drive" kuris atidaro draivo redagavimo puslapi, kuriame leis redaguoti pati draiva.
    Vienas draivas iprastai yra suristas su vienu kompiuteriu. Retais atvejais vienas draivas suristas buna su keliais kompiuteriais. Tokiais atvejais pakeitus sio draivo informacija, pasikeis duomenis visuose kompiuteriuiose kuriuose sis draivas yra priskirtas.
    Issaugojama per "Edit_drive" mygtuko atsidariusiame puslapyje.
* Observation'ai ieskomi, pridedami ir salinami paciame puslapyje. Jei pokytis matosi puslapyje, vadinas tas pokytis ir ivyko.
    Observation'ai ieskomi ivedant i tekstini laukeli raktazodzius ir paspaudus "Enter". Virs tekstinio laukelio islenda lentele su observation'u rezultatais. Sie rezultatai yra atrenkami pagal tai kurie dar nepriskirti kompiuteriui ir atitinka raktazodzius perskirtus tarpais. Siose rezultatu lentelese yra mygtukai "+", jie priskiria atitinkama observation'a prie redaguojamo kompiuterio.
    Observation'ai salinami paspaudus "x" mygtuka prie norimo pasalinti observation'o.

** Trumpa versija: **
* Laikina atmintis, Procesoriai ir Vaizdo plokstes atsinaujina paspaudus issaugojimo mygtuka.
* Draivai per "Edit_drive" mygtuka atsidaranciame puslapyje saugojimi.
* Observation'u sarysiai keiciami javascripto uzklausom. Jeigu matosi pokytis puslapyje, vadinas issaugojimas ivyko.



EN
** Changes in Django server: Added functionality to edit many to many relationships in 5th version computers. **
* RAM allows changing only memory type. Serial, capacity, clock is not allowed to edit, because they should be entered through a client program.
    Saves when pressed saving button.
* Processor Manufacturer, Model, Stock clock, Max clock, Core count and Thread count are allowed to be modified.
    Edited processor is changed only for that computer only, not on all computers where that processor is used on.
    Core count and Thread count are allowed as integers only.
    Saves when pressed saving button.
* GPU Manufacturer and gpu_name are allowed to be modified.
    Edited GPU is changed only for that computer only, not on all computers where that GPU is used on.
    Saves when pressed saving button.
* Drives(HDD/SSD) editing from computer_edit_v5 is not available. Instead there is a button "Edit drive" which opens drive editing, which allows drive editing.
    One drive is usually assigned to a one computer. In rare cases one drive could be assigned to a several computers. In these cases changing drive information, will change data in all computers where that drives is assigned to.
    Saves in "Edit_drive" button's opened page.
* Observations searched, assigned and removed assignation in the same page. If change is visible in page, that means that change has happened.
    Observations are searched by inputing keyword in text box and pressing "Enter". Table with results of observations appears above textbox. These results are selected according to what was unassigned to a present computer and according to a keyword split by spaces. These results in tables have buttons "+", which assigns corresponing observation to a edited computer.
    Observations are removed by pressing "x" button next to observation that needs to be removed.

** Short version: **
* RAMs, Processors and GPUs are edited on pressing save button.
* Drives are saved on page which is opened by pressing "Edit_drive" button.
* Observations relations are changed using javascript calls. If change is visible in the page, that means change has happened.
----------------------------------------------------------------------------------