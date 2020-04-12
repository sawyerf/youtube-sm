NAME	=	youtube-sm

TMP		=	build \
			dist \
			youtube_sm.egg-info

all: $(NAME)

$(NAME):
	python3 setup.py install

clean:
	rm -rf $(TMP)

fclean: clean
	pip3 uninstall -y $(NAME)

upload: fclean
	python3 setup.py sdist bdist_wheel
	python3 -m twine check dist/*
	python3 -m twine upload dist/*

dev: 
	./dev.sh

re: fclean all

.PHONY: all clean fclean re
