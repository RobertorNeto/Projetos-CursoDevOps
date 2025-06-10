#!/bin/bash
#atividade para criar um arquivo de backup com base em uma entrada com uma lista de arquivos ou diretorios.

echo "Manda o array de arquivos"
read -a lista_arquivos

tar -czvf "backup_$(date +%Y-%m-%d).tar.gz" "${lista_arquivos[@]}"

if [ $? -eq 0 ]; then
  echo "Backup Completo"
else
  echo "Erro ao fazer backup"
fi
