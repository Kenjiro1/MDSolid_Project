# Roadmap de Estudo: Análise de Treliças Planas e Sistema de Cálculo

Oct 10, 2026 · @Kenji

## Visão geral

Este roadmap leva o grupo da teoria de treliças planas até um sistema validado, em oito fases sequenciais. O escopo inicial são treliças estaticamente determinadas (isostáticas), o mesmo do módulo Trusses do MDSolids, a menos que o docente peça algo além.

As fases se dividem em duas frentes: teoria estrutural (fases 1 a 3), para justificar os cálculos, e engenharia do sistema (fases 4 a 8), para especificar entradas, validações e testes.

1. Estática e hipóteses da treliça plana
2. Exemplos resolvidos à mão (nós e seções)
3. Método da rigidez (base do algoritmo)
4. MDSolids como especificação funcional
5. Engenharia de software (requisitos, testes, qualidade)
6. Modelo de dados, validação, cálculo e resultados
7. Validação com casos conhecidos
8. Narrativa da apresentação

Cada fase traz objetivo, o que estudar (com link), um guia de passos e um critério de conclusão para você marcar antes de avançar.

## Fase 1: Estática e hipóteses da treliça plana

**Objetivo:** explicar por que uma barra de treliça carrega só força axial e como o equilíbrio dá tração ou compressão.

**Estudar, nesta ordem:**

1. [Engineering Statics: Open and Interactive](https://engineeringstatics.org/) (Baker e Haynes), seção "Trusses". Primeira leitura: modelo plano, hipóteses, estabilidade, membros de força zero. Também está nas [Engineering LibreTexts](<https://eng.libretexts.org/Bookshelves/Mechanical_Engineering/Engineering_Statics:_Open_and_Interactive_(Baker_and_Haynes)>); há [PDF para offline](https://engineeringstatics.org/pdf/statics.pdf).
2. [Structural Analysis, cap. 5: Internal Forces in Plane Trusses](<https://eng.libretexts.org/Bookshelves/Civil_Engineering/Structural_Analysis_(Udoeyo)/01%3A_Chapters/1.05%3A_Internal_Forces_in_Plane_Trusses>) (Udoeyo). Hipóteses, classificação, determinância, reações, convenção de sinais, métodos dos nós e das seções.
3. Aula de apoio do MIT: o documento de origem cita a Lecture 8: Trusses (Ortiz), mas não achei o link direto. Como alternativa, use o material [Trusses, 3.11 Mechanics of Materials](https://ocw.mit.edu/courses/3-11-mechanics-of-materials-fall-1999/resources/mit3_11f99_truss) no MIT OpenCourseWare.

**Guia de passos:**

- [ ] Liste as hipóteses: barras retas, ligadas por articulações, cargas só nos nós, força axial apenas.
- [ ] Desenhe o diagrama de corpo livre da treliça inteira e calcule as reações.
- [ ] Desenhe o diagrama de corpo livre de cada nó.
- [ ] Aprenda a identificar membros de força zero.
- [ ] Verifique a determinância com a contagem abaixo.

Equilíbrio de cada nó e da estrutura inteira:

```latex
\sum F_x = 0, \qquad \sum F_y = 0, \qquad \sum M = 0
```

Verificação preliminar de determinância de treliças planas, com m barras, r componentes de reação e j nós:

```latex
m + r = 2j
```

A contagem sozinha não garante estabilidade: a configuração geométrica também precisa ser estável.

**Concluído quando:** você explica as hipóteses sem consultar, resolve as reações de uma treliça simples e justifica por que ela é isostática.

## Fase 2: Exemplos resolvidos à mão

**Objetivo:** produzir soluções manuais confiáveis, que depois servirão de gabarito para o programa.

**Estudar:** os exemplos do método dos nós e das seções nas mesmas fontes da Fase 1: [Udoeyo, cap. 5](<https://eng.libretexts.org/Bookshelves/Civil_Engineering/Structural_Analysis_(Udoeyo)/01%3A_Chapters/1.05%3A_Internal_Forces_in_Plane_Trusses>) e [Baker e Haynes](https://engineeringstatics.org/). Para texto de livro mais abrangente, use Hibbeler, *Structural Analysis*, 10ª edição (não há link aberto).

**Guia de passos:**

- [ ] Escolha 4 a 5 treliças: uma simples, uma com membro de força zero, uma com cargas inclinadas e uma maior.
- [ ] Resolva cada uma pelo método dos nós, sempre começando por um nó com no máximo duas incógnitas.
- [ ] Confira barras específicas pelo método das seções.
- [ ] Defina e escreva a convenção de sinais do grupo (por exemplo, positivo = tração).
- [ ] Registre para cada exemplo: geometria, cargas, reações e força em cada barra.

**Concluído quando:** cada exemplo tem uma tabela de reações e forças axiais verificada por dois métodos.

## Fase 3: Método da rigidez (base do algoritmo)

**Objetivo:** entender como um programa automatiza a solução montando e resolvendo um sistema matricial.

**Estudar:**

1. [Truss Analysis Using the Stiffness Method](https://www.ce.memphis.edu/4122/notes/pdfs/notes_14a_stifness_method_trusses.pdf) (University of Memphis). É a referência mais alinhada à implementação: graus de liberdade, matriz de rigidez da barra, cossenos diretores, coordenadas globais, montagem e condições de contorno.
2. Hibbeler, *Structural Analysis*, 10ª edição, capítulo do método da rigidez para treliças (referência complementar).

**Ideia central:** monte e resolva

```latex
K \, U = F
```

em que K é a matriz de rigidez da estrutura, U os deslocamentos nodais e F as cargas nodais. Cada barra contribui conforme comprimento, área, módulo de elasticidade e orientação.

**Guia de passos:**

- [ ] Numere nós e graus de liberdade (2 por nó, em treliça plana).
- [ ] Escreva a matriz de rigidez de uma barra e a transformação para coordenadas globais.
- [ ] Monte a matriz da estrutura somando as contribuições por nó.
- [ ] Aplique os vínculos e resolva os deslocamentos desconhecidos.
- [ ] Recupere a força axial em cada barra e as reações.
- [ ] Pós-processamento opcional: tensão normal a partir da força axial e da área, ou área necessária para um limite de tensão.
- [ ] Compare o resultado com seus gabaritos da Fase 2.

**Concluído quando:** você refaz à mão uma treliça pequena pelo método da rigidez e obtém as mesmas forças do método dos nós.

## Fase 4: MDSolids como especificação funcional

**Objetivo:** transformar o comportamento observável do módulo Trusses em uma tabela de requisitos testáveis.

**Estudar:** a [página inicial do MDSolids](https://static-archives.git-pages.mst.edu/mdsolids/home.htm) (Philpot), que lista o módulo de treliças entre os demais. Baixe o programa e use-o como referência de comportamento. Ele se destina a treliças estaticamente determinadas, então limite o escopo inicial a esse caso.

**O que o módulo faz, e que vocês precisam reproduzir:**

- construir uma grade e definir a geometria dos nós;
- desenhar barras ligando nós e verificar a idealização de conexão nos nós;
- inserir apoios e cargas somente nos nós;
- identificar nós automaticamente e exibir ângulos das barras;
- calcular e mostrar tração, compressão e força zero;
- opcionalmente, calcular tensões normais ou dimensionar áreas para um limite de tensão.

**Guia de passos:** converta cada item em uma linha da tabela abaixo (exemplos iniciais) e complete com os demais.

| Função | Dados de entrada | Regra de validação | Resultado esperado | Caso de teste |
| --- | --- | --- | --- | --- |
| Inserir carga | Ponto selecionado, módulo, direção | O ponto deve corresponder a um nó | Carga associada ao nó | Carga fora de nó é rejeitada |
| Calcular treliça válida | Nós, barras, apoios, cargas | Modelo completo e estável | Reações e forças axiais por barra | Treliça simples da Fase 2 |
| Mapear sinal da força | Força axial calculada | Convenção do grupo aplicada | Tração, compressão ou zero exibidos | Exemplo com membro de força zero |

**Concluído quando:** cada função do módulo de referência tem pelo menos um requisito verificável e um caso de teste.

## Fase 5: Engenharia de software

**Objetivo:** escrever requisitos rastreáveis, organizar os testes e discutir a qualidade do sistema além de "calcular certo".

**Estudar:**

| Referência | Para que serve no projeto |
| --- | --- |
| [ISO/IEC/IEEE 29148](https://www.iso.org/standard/72089.html) | Escrever requisitos claros, verificáveis e rastreáveis, ligando necessidades a funções e testes |
| [ISO/IEC/IEEE 29119-2](https://www.iso.org/standard/79428.html) | Organizar testes unitários, de integração, de sistema e de aceitação |
| [ISO/IEC 25010:2023](https://www.iso.org/standard/78176.html) | Discutir completude funcional, facilidade de uso e adequação ao contexto de uso |
| [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html) | Validar tipo, formato e sentido de números, unidades, vínculos, nós e geometria |

As normas ISO são pagas; as páginas acima trazem o resumo e a prévia. Use-as para estruturar o trabalho, sem precisar citar trechos longos.

**Guia de passos:**

- [ ] Reescreva os requisitos da Fase 4 como frases curtas e verificáveis, cada uma com um identificador.
- [ ] Ligue cada requisito a um ou mais casos de teste (rastreabilidade).
- [ ] Classifique os testes em unitários, de integração, de sistema e de aceitação.
- [ ] Escolha 3 características de qualidade da ISO 25010 para discutir na apresentação.
- [ ] Liste as validações de entrada inspiradas no OWASP: tipo, formato e se o valor faz sentido.

**Concluído quando:** existe uma matriz requisito → teste sem requisitos órfãos.

## Fase 6: Modelo de dados, validação, cálculo e resultados

**Objetivo:** definir como o programa representa a treliça e separar as responsabilidades em quatro camadas.

**Arquitetura conceitual:**

1. **Modelo da treliça:** nós com coordenadas; barras com nó inicial e final; apoios; cargas; e, quando necessário, área e módulo de elasticidade.
2. **Validação:** conferir referências a nós existentes, impedir barras de comprimento nulo, aceitar cargas só em nós e verificar se os apoios são suficientes para o caso aceito.
3. **Cálculo:** converter a estrutura validada em equações de equilíbrio ou no sistema matricial, mantendo unidades e convenção de sinais explícitas.
4. **Resultados:** mostrar reações, força axial por barra, classificação em tração, compressão ou zero, e tensão ou área quando implementadas.

**Estudar:** [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html) para as regras de entrada, e a [Fase 3](https://www.ce.memphis.edu/4122/notes/pdfs/notes_14a_stifness_method_trusses.pdf) para o cálculo.

**Guia de passos:**

- [ ] Desenhe o modelo de dados (listas de nós, barras, apoios e cargas).
- [ ] Escreva as regras de validação, uma por requisito da Fase 4.
- [ ] Decida e documente quais casos o programa aceita e quais rejeita.
- [ ] Trate geometria instável ou singular: a contagem de barras sozinha não detecta todos os casos.
- [ ] Defina o formato de saída dos resultados e a convenção visual de sinais.

**Concluído quando:** qualquer entrada inválida produz uma mensagem clara, e a lista de casos aceitos e rejeitados está escrita.

## Fase 7: Validação com casos conhecidos

**Objetivo:** provar que o sistema calcula certo, com evidência registrada.

**Estudar:** [ISO/IEC/IEEE 29119-2](https://www.iso.org/standard/79428.html) como base para estruturar processos e documentação de teste, e seus exemplos manuais da Fase 2 como gabarito.

**Guia de passos:**

- [ ] Rode o programa em cada exemplo da Fase 2 e compare reações e forças com a solução manual.
- [ ] Cubra os casos abaixo, no mínimo.
- [ ] Para cada teste, guarde entrada, resultado esperado, resultado do sistema e critério de aceitação.
- [ ] Corrija as diferenças e repita até todos os testes passarem.

| Caso de teste | O que verifica |
| --- | --- |
| Barra em tração | Sinal e valor da força axial |
| Barra em compressão | Sinal e valor da força axial |
| Membro de força zero | Classificação como zero |
| Carga inclinada | Decomposição em componentes |
| Geometria inválida | Rejeição com mensagem clara |
| Treliça instável ou singular | Detecção além da contagem de barras |

**Concluído quando:** todos os testes têm evidência registrada e o programa concorda com uma solução independente.

## Fase 8: Narrativa da apresentação e checklist final

**Objetivo:** contar o trabalho em cinco passos que respondem a entendimento do modelo, tratamento dos dados, cálculo e interpretação.

1. O que o usuário informa (nós, barras, apoios, cargas).
2. Como os dados viram um modelo (estrutura interna e validações).
3. Quais hipóteses e equações são aplicadas (equilíbrio ou rigidez).
4. Como o software resolve (passos do algoritmo).
5. Como interpretar e verificar o resultado (tração, compressão, zero, testes).

**Checklist final:**

- [ ] Hipóteses da treliça ideal explicadas.
- [ ] Equações essenciais apresentadas: equilíbrio, determinância e, se usado, K U = F.
- [ ] Casos aceitos e rejeitados documentados, incluindo geometria instável.
- [ ] Tabela de requisitos e matriz requisito → teste prontas.
- [ ] Evidências de teste organizadas.
- [ ] Convenção de sinais e unidades explícitas em todos os resultados.

**Concluído quando:** o grupo apresenta a narrativa completa em ordem, sem depender de anotações.

## Referências

| Referência | Fase | Link |
| --- | --- | --- |
| Baker, D. W.; Haynes, W. *Engineering Statics: Open and Interactive*, seção "Trusses" | 1, 2 | [Site do livro](https://engineeringstatics.org/) · [LibreTexts](<https://eng.libretexts.org/Bookshelves/Mechanical_Engineering/Engineering_Statics:_Open_and_Interactive_(Baker_and_Haynes)>) · [PDF](https://engineeringstatics.org/pdf/statics.pdf) |
| Udoeyo, F. *Structural Analysis*, "Internal Forces in Plane Trusses" | 1, 2 | [LibreTexts](<https://eng.libretexts.org/Bookshelves/Civil_Engineering/Structural_Analysis_(Udoeyo)/01%3A_Chapters/1.05%3A_Internal_Forces_in_Plane_Trusses>) |
| Ortiz, C. *Mechanics of Materials*, Lecture 8: Trusses (MIT) | 1 | Link direto não localizado; alternativa: [MIT OCW 3.11, Trusses](https://ocw.mit.edu/courses/3-11-mechanics-of-materials-fall-1999/resources/mit3_11f99_truss) |
| University of Memphis. *Truss Analysis Using the Stiffness Method* | 3, 6 | [PDF](https://www.ce.memphis.edu/4122/notes/pdfs/notes_14a_stifness_method_trusses.pdf) |
| Hibbeler, R. C. *Structural Analysis*, 10ª ed. | 2, 3 | Livro; sem link aberto |
| Philpot, T. A. MDSolids, módulo Trusses | 4 | [Página do MDSolids](https://static-archives.git-pages.mst.edu/mdsolids/home.htm) |
| ISO/IEC/IEEE 29148, engenharia de requisitos | 5 | [ISO](https://www.iso.org/standard/72089.html) |
| ISO/IEC/IEEE 29119-2, processos de teste | 5, 7 | [ISO](https://www.iso.org/standard/79428.html) |
| ISO/IEC 25010:2023, modelo de qualidade de produto | 5 | [ISO](https://www.iso.org/standard/78176.html) |
| OWASP Input Validation Cheat Sheet | 5, 6 | [OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html) |
