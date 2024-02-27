/**
 * Base de dados para persistência da informção
 * de materiais apreendidos
 */

DROP TABLE IF EXISTS material;
DROP TABLE IF EXISTS termo_entrega;
DROP TABLE IF EXISTS auto;
DROP TABLE IF EXISTS tipo_material;
DROP TABLE IF EXISTS fabricante;
DROP TABLE IF EXISTS armazem;
DROP TABLE IF EXISTS termo_entrega;
DROP TYPE IF EXISTS TIPO_AUTO;
DROP TYPE IF EXISTS TIPO_TERMO_ENTREGA;
DROP TYPE IF EXISTS ESTADO_MATERIAL;
DROP TYPE IF EXISTS EXAME_MATERIAL;

CREATE TABLE tipo_material (
  codigo VARCHAR(4) NOT NULL PRIMARY KEY,
  descricao VARCHAR(100) NOT NULL
);

CREATE TABLE fabricante (
  codigo VARCHAR(4) NOT NULL PRIMARY KEY,
  descricao VARCHAR(100) NOT NULL
);

CREATE TABLE armazem (
  codigo VARCHAR(4) NOT NULL PRIMARY KEY,
  descricao VARCHAR(100) NOT NULL
);

CREATE TYPE TIPO_AUTO AS ENUM ('Auto-noticia crime', 'Auto-apreensao','Auto-noticia C O');
CREATE TYPE TIPO_TERMO_ENTREGA AS ENUM ('Entrada', 'Entrega Arguido','Entrega Entidade', 'Destruição');
CREATE TYPE ESTADO_MATERIAL AS ENUM ('Destruido', 'Entregue Arguido','Reverte Entidades','Armazem');
CREATE TYPE EXAME_MATERIAL AS ENUM ('Exame Efectuado', 'Efectuar Exame','Não é necessário', 'Não preenchido');

CREATE TABLE auto (
    id SERIAL NOT NULL PRIMARY KEY,
    ano_processo INTEGER NOT NULL,
    num_processo INTEGER NOT NULL,
    nuipc VARCHAR(20), -- Numero unico de Processo Crime
    contra_ordenacao VARCHAR(20),
    num_auto INTEGER NOT NULL,
    tipo TIPO_AUTO,
    data DATE,
    data_recepcao_igc DATE,
    data_recepcao_armazem DATE,
    data_registo DATE
);

CREATE TABLE termo_entrega (
    id SERIAL NOT NULL PRIMARY KEY,
    id_auto INTEGER NOT NULL REFERENCES auto(id),
    num_termo INTEGER,
    data_registo DATE,
    data_termo DATE,
    tipo_termo_entrega TIPO_TERMO_ENTREGA,
    cod_entidade INTEGER,
    cod_meio_humano INTEGER
);

CREATE TABLE material (
    id SERIAL NOT NULL PRIMARY KEY,
    id_auto INTEGER NOT NULL REFERENCES auto(id),
    id_termo_entrada INTEGER NOT NULL REFERENCES termo_entrega(id),
    id_termo_saida INTEGER REFERENCES termo_entrega(id),
    estadoMaterial ESTADO_MATERIAL,
    exameMaterial EXAME_MATERIAL,
    id_tipo_material VARCHAR(4) NOT NULL REFERENCES tipo_material(codigo),
    descricao VARCHAR(250),
    quantidade INTEGER,
    fila VARCHAR(10),
    lugar VARCHAR(10),
    prateleira VARCHAR(10),
    cor VARCHAR(20),
    id_fabricante VARCHAR(4) REFERENCES fabricante(codigo),
    id_armazem VARCHAR(4) REFERENCES armazem(codigo)
);
