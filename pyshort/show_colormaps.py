#!/usr/bin/env python

from matplotlib import cm as mcm
from matplotlib import pyplot as pp
import numpy as np

def main():
	vals = np.outer(np.ones(10), np.linspace(0.0, 1.0, num=100))
	cmaps = [cm_name for cm_name in mcm.datad if not cm_name.endswith('_r')]
	cmaps.sort()
	pp.figure(figsize=(7, 11))
	pp.subplots_adjust(top=0.8, bottom=0.05, left=0.01, right=0.99)
	for i, cm_name in enumerate(cmaps):
		pp.subplot(len(cmaps), 1, i + 1)
		pp.axis('off')
		pp.imshow(vals, aspect='auto', cmap=pp.get_cmap(cm_name))
		pp.text(101, 9, cm_name, fontdict={'size': 8})
	pp.savefig('cmaps.png', dpi=200, facecolor='gray', bbox_inches='tight')


if __name__ == '__main__':
	main()

