# Generated by Django 4.1.2 on 2022-10-29 00:35

import cpf_field.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('primeiro_nome', models.CharField(max_length=100)),
                ('ultimo_nome', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('telefone', models.CharField(max_length=100)),
                ('data_nascimento', models.DateField()),
                ('cpf', cpf_field.models.CPFField(max_length=11, unique=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Carrinho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.FloatField(default=0)),
                ('cliente', models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Cartao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=100)),
                ('nome', models.CharField(max_length=100)),
                ('validade', models.CharField(max_length=100)),
                ('codigo', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rua', models.CharField(max_length=100)),
                ('numero', models.IntegerField()),
                ('bairro', models.CharField(max_length=100)),
                ('cep', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.CharField(max_length=100)),
                ('preco', models.FloatField()),
                ('thumbnail', models.ImageField(default='', upload_to='imagens/', verbose_name='Imagem')),
                ('estoque', models.IntegerField()),
                ('marca', models.CharField(max_length=100)),
                ('categoria', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='cadastro.categoria', verbose_name='Categoria')),
            ],
        ),
        migrations.CreateModel(
            name='UnidadeFederativa',
            fields=[
                ('codigo', models.CharField(max_length=2, primary_key=True, serialize=False)),
                ('sigla', models.CharField(max_length=2, unique=True)),
                ('nome', models.CharField(max_length=60, unique=True)),
            ],
            options={
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='ProdutoImagens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagens', models.FileField(upload_to='imagens/')),
                ('produto', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='cadastro.produto', verbose_name='Produto')),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('1', 'Pendente'), ('2', 'Aprovado'), ('3', 'Cancelado'), ('4', 'Entregue')], default='1', max_length=1)),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('total', models.FloatField(default=0)),
                ('carrinho', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='cadastro.carrinho', verbose_name='Carrinho')),
                ('cliente', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Cliente')),
                ('endereco', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='cadastro.endereco', verbose_name='Endereço')),
            ],
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=6, unique=True)),
                ('nome', models.CharField(max_length=60)),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='municipios', to='cadastro.unidadefederativa')),
            ],
        ),
        migrations.CreateModel(
            name='ItemCarrinho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.IntegerField()),
                ('subtotal', models.FloatField(default=0)),
                ('carrinho', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='cadastro.carrinho', verbose_name='Carrinho')),
                ('produto', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='cadastro.produto', verbose_name='Produto')),
            ],
        ),
        migrations.AddField(
            model_name='endereco',
            name='cidade',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='cadastro.municipio', verbose_name='Cidade'),
        ),
        migrations.AddField(
            model_name='endereco',
            name='cliente',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Cliente'),
        ),
        migrations.AddField(
            model_name='endereco',
            name='estado',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='cadastro.unidadefederativa', verbose_name='Estado'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='cartao',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='cadastro.cartao', verbose_name='Cartão'),
        ),
    ]