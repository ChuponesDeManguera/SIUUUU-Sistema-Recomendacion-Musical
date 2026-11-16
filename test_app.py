import unittest
from app import recomendar,jaccard,app
class Pruebas(unittest.TestCase):
 def test_genero(self):
  self.assertEqual({c['id'] for c in recomendar(generos={'rock'})},{'c1','c3'})
 def test_artista(self):
  self.assertEqual({c['id'] for c in recomendar(artistas={'Nova'})},{'c2','c3'})
 def test_exclusion(self):
  self.assertEqual([c['id'] for c in recomendar(generos={'rock'},seleccionadas={'c1'})],['c3'])
 def test_vacio(self):
  self.assertEqual(recomendar(),[])
 def test_sin_coincidencia(self):
  self.assertEqual(recomendar(generos={'clasica'}),[])
 def test_doble_coincidencia(self):
  self.assertEqual(recomendar(generos={'rock'},artistas={'Nova'})[0]['id'],'c3')
 def test_jaccard_vacio(self):
  self.assertEqual(jaccard(set(),set()),0)
 def test_no_duplicados(self):
  self.assertEqual(len(recomendar(generos=['rock','rock'])),2)
 def test_catalogo(self):
  self.assertTrue(all(c['id'] in {f'c{i}' for i in range(1,7)} for c in recomendar(generos={'pop'})))
 def test_web(self):
  self.assertEqual(app.test_client().get('/').status_code,200)
if __name__=='__main__': unittest.main(verbosity=2)
