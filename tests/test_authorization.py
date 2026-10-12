


def test_usuario_no_puede_crear_libro(client,libro_data,usuario_headers):
    response=client.post(
            "/libros",
            json=libro_data,headers=usuario_headers
        )
    data=response.json()

    assert response.status_code == 403
    assert data['detail'] == 'Usuario no Autorizado'


def test_usuario_no_puede_actualizar_libro(client,libro_data,admin_autenticado,usuario_headers):
    response=client.post(
                "/libros",
                json=libro_data,headers=admin_autenticado['headers']
            )
    data=response.json()

    assert response.status_code == 201
    libro_id=data['id']

    response2=client.patch(f'/libros/{libro_id}',json={'precio':30},headers= usuario_headers)
    data2= response2.json()

    assert response2.status_code == 403
    assert data2['detail'] == 'Usuario no Autorizado'


def test_usuario_no_puede_eliminar_libro(client,libro_data, admin_autenticado,usuario_headers):
    response=client.post(
                "/libros",
                json=libro_data,headers=admin_autenticado['headers']
            )
    data=response.json()
    assert response.status_code == 201
    libro_id=data['id']

    response2=client.delete(f'/libros/{libro_id}',headers=usuario_headers)
    data2=response2.json()

    assert response2.status_code == 403
    assert data2['detail'] == 'Usuario no Autorizado'
