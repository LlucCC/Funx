# Funx

Funx és un llenguatge de programació interpretat orientat a expressions i funcions.

Aquest projecte està orientat a crear un intèrpret de funx que es pugi executar en un entorn web i permeti fer totes les operacions que permeti funx.

En la carpeta del projecte podreu trobar:
    - README.md: En aquest document trobareu la documentació del projecte
    - funx.py: El codi font de l'intèrpret, amb tot el necesari per compilar i executar-lo 
    - funx.g4: La gramàtica del llenguatge. Podeu fer-li un ull si voleu veure tot el que permet funx.
    - test-OperacionsBooleanes.funx: Exemples de codi que permeten provar la extensió de les operacions booleanes
    - test-OrdreSuperior.funx: Exemples de codi que permetern provar la extensió de les funcions d'ordre superior
    - templates: Carpeta que només conté l'arxiu base.html, que és el codi html per a visualitzar l'intèrpret

## Funcionament del llenguatge

L'intèrpret de funx pot rebre una cadena de definicions de funcions amb, opcionalment, una expressió al final.
En el moment en el que l'intèrpret rep una expressió, l'executa i retorna el seu resultat.

Una expressió pot ser una operació aritmética (les operacions disponibles són: '/', '+', '-', '%', '*' i '^'), una variable, un número, una crida a una funció o qualsevol combinació d'altres expressions.

En l'exemple següent es pot veure clarament una expressió:

```
 x * (y + (F 3))
 #On F és una funció
```
Els noms de les variables sempre comencen amb una lletra minúscula, els noms de les funcions amb una majúscula i els comentaris amb #. 

Les variables no s'han de definir per utilitzar-les, totes les variables tenen 0 com a valor per defecte i, si es desitja, és pot assignar un valor a una variable amb l'operand '<-' (s'utilitza: x <- expressió). A més, totes les variables són nombres enters, funx no permet la definició de tipus.

Si es vol definir una funció només cal escriure el seu nom, seguit dels parametres que rebrà la funció, seguit de la definició de la funció entre {}

```
Suma x y {
    x + y
}

Suma 2 3
#Out: 5
```

En l'exemple anterior es pot veure clarament la definició de la funció suma amb la seva posterior invocació.

És important tenir en compte que no existeix la comanda "return" a funx, en el seu lloc, la funció retorna el valor de la primera expressió que trobi (cal destacar que una assignació no és una expressió i per tant es poden utilitzar sense que es forci a la funció a retornar un valor).

Per exemple, en l'exemple de suma es retorna el resultat de la expressió "x + y", la primera expressió que troba.

```
OperacioExtranya x y z{
    x1 <- y + z
    y1 <- y + x
    z1 <- z + x
    x1 * y1 * z1
}
```

En aquest exemple la funció retorna x1 * y1 * z1, ja que és la primera expressió que es troba. Les assignacions previes no retornen cap valor, i, per tant, el programa no es para al executarles.

Adicionalment, funx també permet utilitzar condicionals i bucles while. De la mateixa manera que un bloc de funció, un bloc d'un condicional o d'un bucle (definits també amb {}) retornarà un valor si executa una expressió dins del seu bloc, per exemple:

```
Factorial n {
    if n == 0 {
        1
    }

    else {n * Factorial (n - 1)}
    #El bloc else es opcional i es podria no posar
}
```

En aquest exemple la funció Factorial tindrà 2 punts de sortida, pot retorar l'1 o la expressió n * Factorial (n - 1). Els bucles funcionen de forma anàloga, si s'executa una expressió que retorni algun valor dins d'un bucle while, es retornarà aquell valor i es sortirà de la funció.

A funx no existeixen les variables booleanes, aixì que qualsevol condició per als condicionals i els bucles s'ha d'expressar com a comparació d'enters (amb els operands: '==', '<' '>' '>=' i '<=') amb la opció d'afegir operadors lògics entre comparacions (explicat amb més detall en l'apartat d'extensions).

Un últim detall de funx és que totes les variables tenen com a àmbit de visibilitat la funció on estan declarades. És a dir, totes les variables que s'utilitzen dins d'una funció son locals a la funció (no existeixen variables globals ni es poden pasar paràmetres per referència), i els condicionals i bucles que es defineixin dins de la funció tampoc generen nous àmbits de visibilitat, les varibales declarades dins d'un condicional o un bucle es poden veure des de fora.

Com ja s'ha explicat, no es poden definir variables globals, però si hi ha una manera de definir "constants" globals. Es poden utilitzar funcions per aconseguir aquest propòsit:

```
PI {
    3 
    #Utilitzem 3 com a constant per el número pi perque funx nomès treballa amb enters
}

CalculaAreaCercle r {
  PI * r * r
}
```

## Invocació de l'intérpret

El primer pas serà compilar la gramàtica d'ANTLR4 amb la comanda:

```sh
antlr4 -Dlanguage=Python3 -no-listener -visitor funx.g4  
```

Seguidament, per utiltizar l'intèrpret només caldrà utilitzar les següents comandes des d'aquesta carpeta (carpeta funx):

```sh
export FLASK_APP=funx
flask run
```

Cal destacar que l'usuari que desitgi executar l'intèrpret de funx haurà de tenir flask instalat al seu ordinador.

Un cop s'executin aquestes comandes s'haurà d'accedir a la direcció http://127.0.0.1:5000

## Funcionament de l'intèrpret

Al obrir per primera vegada la pàgina web, es poden trobar 3 zones diferents: Results, Functions i una consola.

La consola serveix per introduir codi en funx per a que sigui interpretat per l'intèrpret. Al clicar el botó d'execute de la consola s'executarà el codi introduit i el seu resultat, si no és nul, apraeixerà a la secció de resultats.

La secció de resultats (Results) conté les 5 últimes entrades que han retornat alguna cosa amb els seus respectius resultats. Si l'entrada no conté cap expressió (només declaracions de funcions), el valor de retorn és nul i, per tant, no es mostrarà en la part de resultats.

Cal destacar que al introduir codi gramaticalment incorrecte, no hi haurà cap valor de retorn i, per tant, no es mostrarà cap resultat. Si es produeixen errors en execució (divisió per 0, variables repetides 
en la capçalera de la funció...) llavors s'informarà a l'usuari de l'error.

La secció Functions conté totes les funcions que han sigut definides i, per tant, es poden utilitzar en noves entrades de codi. 

Finalment la pàgina web conté un botó adicional, "Toggle Dark/Light Theme", que, com el seu nom indica, canvia entre el mode clar i fosc de la pàgina web. Simplement canvia l'apariència de la web i és una funcionalitat completament estètica.

## Extensions

A la definició original de funx s'han afegit 2 extensions: Operadors lògics i funcions d'ordre superior

# Operadors lògics

Per a facilitar l'escritura de condicions s'han afegit els opradors lògics habituals ('not', 'and' i 'or') per a que es pugin utilitzar en combinació amb les expressions booleanes. A més dels operadors habituals s'han inclòs 3 adicionals: 'xor', '->', '<->'. a xor b retorna cert si a i b tenen valors diferents (un és cert i l'altre és fals), a <-> b significa equivalència entre a i b (Els dos certs o els dos falsos) i a -> b significa implicació (si a és cert llavors b també o ha de ser).

El següent és un exemple de l'ús d'aquests operadors (s'inclouen més en el fitzer test-OperacionsBooleanes.funx)

```
Fibo n {
    if n == 0 or n == 1 {n}
    (Fibo n - 1) + (Fibo n - 2)
}
```

Com es veu en l'exemple, l'operador lògic 'or' s'utilitza entre 2 expressions booleanes i dona com a resultat una nova expressió booleana. Cal destacar que ni els operadors de comparacions ni els nous operadors lògics es poden utilitzar com a expressió normal i nomès apareixen en el context de condicions de bucles o condicionals.

# Funcions d'ordre superior

Gràcies a una extensió, funx permet la declaració i utilització de funcions d'ordre superior, és a dir, es poden utilitzar funcions com a paràmetres d'altres funcions. Una funció que rep altres funcions és exactament igual a una funció normal de funx, però en la seva declaració s'utilitzen identificadors de paràmetres que comencin en majúscula per indicar que es tracta d'una nova funció (és important que no existeixi cap funció amb el nom del paràmetre per evitar conflictes).

Al cridar una funció d'ordre superior simplement se li ha de pasar una funció ja definida com a paràmetre. Si enlloc d'una funció es pasa una variable o un nom de funció no definida es produirà un error.

En el següent exemple es declara una funció NApply que aplica n vegades una funció F sobre un paràmetre x:

```
NApply F n x {
    i <- 0
    res <- x
    while i < n {
        res <- F res
        i <- i + 1
    }
    res
}
```
Podeu trobar més exemples en l'arxiu test-OrdreSuperior.funx
## Agraïments

M'agradaria donar gràcies a Gerard Escudero per ajudar-me en la creació de l'intèrpret i resoldre els dubtes que m'han anat sorgint, al professorat d'LP per fer les transparències de l'assignatura (que han sigut un recurs molt valuós), i a ChatGPT3, una inteligència artificial que m'ha resolt tots els dubtes que tenia sobre HTML i CSS.