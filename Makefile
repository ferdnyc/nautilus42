# Makefile for source rpm: nautilus
# $Id$
NAME := nautilus
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
