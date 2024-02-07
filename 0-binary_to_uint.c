#include "main.h"
#include <string.h>


/**
 * binary_to_uint - converts a binary number to unsigned intteger
 * @b: pointer to string of binary number
 *
 * Return: unsigned integer else 0
 */
unsigned int binary_to_uint(const char *b)
{
	unsigned int n;

	n = 0;
	if (b == NULL)
		return (0);
	for (; *b != '\0'; b++)
	{
		if ((*b - '0') > 1 || (*b - '0') < 0)
			return (0);
		n = n * 2 + (*b - '0');
	}
	return (n);
}
